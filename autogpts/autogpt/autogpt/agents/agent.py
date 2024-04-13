import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional

import pydantic
from pydantic import Field

import autogpt.config as config
import autogpt.core.configuration as core_configuration
import autogpt.core.prompting as core_prompting
import autogpt.core.resource.model_providers as model_providers
import autogpt.logs.log_cycle as log_cycle
import autogpt.logs.utils as log_utils
import autogpt.models.action_history as action_history
import autogpt.models.command as command_module
import autogpt.models.context_item as context_item
import autogpt.models.context as context_model
import autogpt.models.plugin as plugin_model
import autogpt.prompt_strategies.one_shot as one_shot_prompt
from autogpt.core.exceptions import AgentException, AgentTerminated
from autogpt.core.resource.model_providers import ChatModelProvider
from autogpt.llm.api_manager import ApiManager

logger = logging.getLogger(__name__)


class AgentConfiguration(core_configuration.BaseAgentConfiguration):
    pass


class AgentSettings(core_configuration.BaseAgentSettings):
    config: AgentConfiguration = Field(default_factory=AgentConfiguration)
    prompt_config: one_shot_prompt.OneShotAgentPromptConfiguration = Field(
        default_factory=(
            lambda: one_shot_prompt.OneShotAgentPromptStrategy.default_configuration.copy(deep=True)
        )
    )


class Agent(
    context_model.ContextMixin,
    context_item.FileWorkspaceMixin,
    context_item.WatchdogMixin,
    command_module.BaseAgent,
    core_configuration.Configurable[AgentSettings],
):
    """AutoGPT's primary Agent; uses one-shot prompting."""

    default_settings: AgentSettings = AgentSettings(
        name="Agent",
        description=__doc__,
    )

    prompt_strategy: one_shot_prompt.OneShotAgentPromptStrategy

    def __init__(
        self,
        settings: AgentSettings,
        llm_provider: ChatModelProvider,
        command_registry: command_module.CommandRegistry,
        legacy_config: config.Config,
    ):
        prompt_strategy = one_shot_prompt.OneShotAgentPromptStrategy(
            configuration=settings.prompt_config,
            logger=logger,
        )
        super().__init__(
            settings=settings,
            llm_provider=llm_provider,
            prompt_strategy=prompt_strategy,
            command_registry=command_registry,
            legacy_config=legacy_config,
        )

        self.created_at = datetime.now().strftime("%Y%m%d_%H%M%S")
        """Timestamp the agent was created; only used for structured debug logging."""

        self.log_cycle_handler = log_cycle.LogCycleHandler()
        """LogCycleHandler for structured debug logging."""

    def build_prompt(
        self,
        *args,
        extra_messages: Optional[list[core_prompting.ChatMessage]] = None,
        include_os_info: Optional[bool] = None,
        **kwargs,
    ) -> core_prompting.ChatPrompt:
        if not extra_messages:
            extra_messages = []

        # Clock
        extra_messages.append(
            core_prompting.ChatMessage.system(f"The current time and date is {time.strftime('%c')}")
        )

        # Add budget information (if any) to prompt
        api_manager = ApiManager()
        if api_manager.get_total_budget() > 0.0:
            remaining_budget = (
                api_manager.get_total_budget() - api_manager.get_total_cost()
            )
            if remaining_budget < 0:
                remaining_budget = 0

            budget_msg = core_prompting.ChatMessage.system(
                f"Your remaining API budget is ${remaining_budget:.3f}"
                + (
                    " BUDGET EXCEEDED! SHUT DOWN!\n\n"
                    if remaining_budget == 0
                    else " Budget very nearly exceeded! Shut down gracefully!\n\n"
                    if remaining_budget < 0.005
                    else " Budget nearly exceeded. Finish up.\n\n"
                    if remaining_budget < 0.01
                    else ""
                ),
            )
            logger.debug(budget_msg)
            extra_messages.append(budget_msg)

        return super().build_prompt(
            *args,
            extra_messages=extra_messages,
            include_os_info=include_os_info,
            **kwargs,
        )

    def on_before_think(self, *args, **kwargs) -> core_prompting.ChatPrompt:
        prompt = super().on_before_think(*args, **kwargs)

        self.log_cycle_handler.log_count_within_cycle = 0
        self.log_cycle_handler.log_cycle(
            self.ai_profile.ai_name,
            self.created_at,
            self.config.cycle_count,
            prompt
