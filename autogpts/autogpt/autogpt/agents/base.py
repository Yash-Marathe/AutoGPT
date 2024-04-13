import collections
import dataclasses
import enum
import logging
import os
import sys
import typing
from abc import ABC, abstractmethod
from pathlib import Path

import pydantic

if typing.TYPE_CHECKING:
    from autogpt.config import Config
    from autogpt.core.prompting.base import PromptStrategy
    from autogpt.core.resource.model_providers.schema import (
        AssistantChatMessageDict,
        ChatModelInfo,
        ChatModelProvider,
        ChatModelResponse,
    )
    from autogpt.models.command_registry import CommandRegistry

from autogpt.agents.utils.prompt_scratchpad import PromptScratchpad
from autogpt.config import ConfigBuilder
from autogpt.config.ai_directives import AIDirectives
from autogpt.config.ai_profile import AIProfile
from autogpt.core.configuration import (
    Configurable,
    SystemConfiguration,
    SystemSettings,
    UserConfigurable,
)
from autogpt.core.prompting.schema import (
    ChatMessage,
    ChatPrompt,
    CompletionModelFunction,
)
from autogpt.core.resource.model_providers.openai import (
    OPEN_AI_CHAT_MODELS,
    OpenAIModelName,
)
from autogpt.llm.providers.openai import get_openai_command_specs
from autogpt.models.action_history import ActionResult, EpisodicActionHistory
from autogpt.prompts.prompt import DEFAULT_TRIGGERING_PROMPT

logger = logging.getLogger(__name__)

CommandName = str
CommandArgs = dict[str, str]
AgentThoughts = dict[str, Any]

class OpenAIModelNameLiteral(enum.Enum):
    GPT3_16k = "gpt-3.5-turbo-16k"
    GPT4 = "gpt-4"

class BaseAgentConfiguration(SystemConfiguration):
    allow_fs_access: bool = UserConfigurable(default=False)

    fast_llm: OpenAIModelNameLiteral = UserConfigurable(default=OpenAIModelNameLiteral.GPT3_16k)
    smart_llm: OpenAIModelNameLiteral = UserConfigurable(default=OpenAIModelNameLiteral.GPT4)
    use_functions_api: bool = UserConfigurable(default=False)

    default_cycle_instruction: str = DEFAULT_TRIGGERING_PROMPT

    big_brain: bool = UserConfigurable(default=True)

    cycle_budget: typing.Optional[int] = 1
    cycles_remaining = cycle_budget
    cycle_count = 0

    send_token_limit: typing.Optional[int] = None
    summary_max_tlength: typing.Optional[int] = None

    plugins: list[typing.Type[AutoGPTPluginTemplate]] = dataclasses.field(
        default_factory=list,
        exclude=True,
    )

    @dataclasses.validator("plugins", each_item=True)
    def validate_plugins(cls, v: typing.Type[AutoGPTPluginTemplate] | Any):
        assert issubclass(
            v,
            AutoGPTPluginTemplate,
        ), f"{v} does not subclass AutoGPTPluginTemplate"
        assert (
            v.__name__ != "AutoGPTPluginTemplate"
        ), f"Plugins must subclass AutoGPTPluginTemplate; {v} is a template instance"
        return v

    @dataclasses.validator("use_functions_api")
    def validate_openai_functions(cls, v: bool, values: dict[str, Any]):
        if v:
            smart_llm = values["smart_llm"]
            fast_llm = values["fast_llm"]
            assert all(
                [
                    not any(s in name.value for s in {"-0301", "-0314"})
                    for name in {smart_llm, fast_llm}
                ]
            ), (
                f"Model {smart_llm.value} does not support OpenAI Functions. "
                "Please disable OPENAI_FUNCTIONS or choose a suitable model."
            )
        return v

class BaseAgentSettings(SystemSettings):
    agent_id: str = ""
    agent_data_dir: typing.Optional[Path] = None

    ai_profile: AIProfile = AIProfile(ai_name="AutoGPT")
    directives: AIDirectives = AIDirectives.from_file(
        ConfigBuilder.default_settings.prompt_settings_file
    )
    task: str = "Terminate immediately"

    config: BaseAgentConfiguration = BaseAgentConfiguration()
    history: EpisodicActionHistory = EpisodicActionHistory()

    def save_to_json_file(self, file_path: Path) -> None:
        with file_path.open("w") as f:
            f.write(self.json())

    @classmethod
    def load_from_json_file(cls, file_path: Path):
        return cls.parse_file(file_path)

class ThoughtProcessOutput(typing.NamedTuple):
    command_name: CommandName
    command_args: CommandArgs
    agent_thoughts: AgentThoughts

class BaseAgent(Configurable[BaseAgentSettings], ABC):
    ThoughtProcessOutput = ThoughtProcessOutput

    default_settings = BaseAgentSettings(
       
