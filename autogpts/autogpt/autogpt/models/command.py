from __future__ import annotations

import inspect
from typing import AnyCallable, Callable, Literal, Optional, TypeVar

from typing_extensions import Annotated

from .command_parameter import CommandParameter
from .context_item import ContextItem

CommandReturnValue = TypeVar("CommandReturnValue")
CommandOutput = Annotated[CommandReturnValue | tuple[CommandReturnValue, ContextItem], "CommandOutput"]

class Command:
    """A class representing a command.

    Attributes:
        name (str): The name of the command.
        description (str): A brief description of what the command does.
        method (Callable): The method that the command executes.
        parameters (list): The parameters of the method.
        enabled (bool | Callable): Whether the command is enabled or not.
        disabled_reason (Optional[str]): The reason why the command is disabled.
        aliases (list[str]): The aliases of the command.
        available (bool | Callable): Whether the command is available or not.
    """

    def __init__(
        self,
        name: str,
        description: str,
        method: Callable[..., CommandOutput],
        parameters: list[CommandParameter],
        enabled: bool | Callable[[], bool] = True,
        disabled_reason: Optional[str] = None,
        aliases: list[str] = [],
        available: bool | Callable[[], bool] = True,
    ):
        self.name = name
        self.description = description
        self.method = method
        self.parameters = parameters
        self.enabled = enabled
        self.disabled_reason = disabled_reason
        self.aliases = aliases
        self.available = available

    @property
    def is_async(self) -> bool:
        return inspect.iscoroutinefunction(self.method)

    def __call__(self, *args: Any, agent: Any = None, **kwargs: Any) -> CommandReturnValue:
        if callable(self.enabled) and not self.enabled():
            if self.disabled_reason:
                raise RuntimeError(
                    f"Command '{self.name}' is disabled: {self.disabled_reason}"
                )
            raise RuntimeError(f"Command '{self.name}' is disabled")

        if callable(self.available) and not self.available():
            raise RuntimeError(f"Command '{self.name}' is not available")

        return self.method(*args, **kwargs, agent=agent)

    def __str__(self) -> str:
        params = [
            f"{param.name}: "
            + ("%s" if param.spec.required else "Optional[%s]") % param.spec.type.value
            for param in self.parameters
        ]
        return (
            f"{self.name}: {self.description.rstrip('.')}. "
            f"Params: ({', '.join(params)})"
        )
