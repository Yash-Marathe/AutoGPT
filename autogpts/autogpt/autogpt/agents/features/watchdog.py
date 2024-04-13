from __future__ import annotations

import logging
import hashlib
from contextlib import ExitStack
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from autogpt.base import BaseAgentConfiguration
    from autogpt.models.action_history import EpisodicActionHistory
    from autogpt.base import BaseAgent

logger = logging.getLogger(__name__)


class WatchdogMixin:
    """
    Mixin that adds a watchdog feature to an agent class. Whenever the agent starts
    looping, the watchdog will switch from the FAST_LLM to the SMART_LLM and re-think.
    """

    config: Optional[BaseAgentConfiguration]
    event_history: EpisodicActionHistory

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if not isinstance(self, BaseAgent):
            raise NotImplementedError(
                f"{__class__.__name__} can only be applied to BaseAgent derivatives"
            )

        self.check_config()

    def check_config(self) -> None:
        if self.config is None:
            raise ValueError("config must be provided")

    async def propose_action(
        self, *args, **kwargs
    ) -> BaseAgent.ThoughtProcessOutput:
        command_name, command_args, thoughts = await super().propose_action(*args, **kwargs)

        if not self.config.big_brain and self.config.fast_llm != self.config.smart_llm:
            if not command_name:
                rethink_reason = "AI did not specify a command"
            else:
                previous_cycle = self.event_history.episodes[-2] if self.event_history else None
                previous_command = previous_cycle.action.name if previous_cycle else None
                previous_command_args_hash = hashlib.md5(
                    repr(previous_cycle.action.args).encode()
                ).hexdigest() if previous_cycle else ""
                current_command_args_hash = hashlib.md5(
                    repr(command_args).encode()
                ).hexdigest()

                if previous_command == command_name and previous_command_args_hash == current_command_args_hash:
                    rethink_reason = f"Repetitive command detected ({command_name})"
                else:
                    rethink_reason = ""

            if rethink_reason:
                logger.info(f"{rethink_reason}, re-thinking with SMART_LLM...")
                if not self.big_brain:
                    with ExitStack() as stack:
                        @stack.callback
                        def restore_state() -> None:
                            # Executed after exiting the ExitStack context
                            self.config.big_brain = False

                        # Remove partial record of current cycle
                        self.event_history.rewind()

                        # Switch to SMART_LLM and re-think
                        self.config.big_brain = True
                        return await self.propose_action(*args, **kwargs)

        return command_name, command_args, thoughts
