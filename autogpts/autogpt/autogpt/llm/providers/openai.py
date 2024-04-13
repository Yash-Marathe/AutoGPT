from __future__ import annotations

import logging
from typing import Callable, Iterable, TypeVar

from autogpt.core.resource.model_providers import CompletionModelFunction
from autogpt.models.command import Command

T = TypeVar("T", bound=Callable)

logger = logging.getLogger(__name__)

def get_function_specs(commands: Iterable[Command]) -> list[CompletionModelFunction]:
    """Get function specs for the agent's available commands.
    This can be used for any completion model that supports function calling.
    """
    return [
        CompletionModelFunction(
            name=command.name,
            description=command.description,
            parameters={param.name: param.spec for param in command.parameters},
        )
        for command in commands
    ]

def get_openai_command_specs(commands: Iterable[Command]) -> list[CompletionModelFunction]:
    """Get OpenAI-consumable function specs for the agent's available commands.
    see https://platform.openai.com/docs/guides/gpt/function-calling
    """
    function_specs = get_function_specs(commands)
    # Add any OpenAI-specific modifications to the function_specs here
    return function_specs
