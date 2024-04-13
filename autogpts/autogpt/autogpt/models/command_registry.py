from __future__ import annotations

import importlib
import inspect
import logging
from dataclasses import dataclass, field
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional, Type, Union

if TYPE_CHECKING:
    from autogpt.agents.base import BaseAgent
    from autogpt.config import Config


from autogpt.command_decorator import AUTO_GPT_COMMAND_IDENTIFIER
from autogpt.models.command import Command

logger = logging.getLogger(__name__)


@dataclass
class CommandRegistry:
    """
    The CommandRegistry class is a manager for a collection of Command objects.
    It allows the registration, modification, and retrieval of Command objects,
    as well as the scanning and loading of command plugins from a specified
    directory.
    """

    commands: Dict[str, Command] = field(default_factory=dict)
    commands_aliases: Dict[str, Command] = field(default_factory=dict)
    categories: Dict[str, CommandCategory] = field(default_factory=dict)

    @dataclass
    class CommandCategory:
        name: str
        title: str
        description: str
        commands: List[Command] = field(default_factory=list)
        modules: List[ModuleType] = field(default_factory=list)

        def __str__(self):
            return f"{self.name} ({len(self.commands)} commands)"

    def __contains__(self, command_name: str):
        return command_name in self.commands or command_name in self.commands_aliases

    def _import_module(self, module_name: str) -> Any:
        return importlib.import_module(module_name)

    def _reload_module(self, module: Any) -> Any:
        return importlib.reload(module)

    def register(self, cmd: Command) -> None:
        if cmd.name in self.commands:
            logger.warning(
                f"Command '{cmd.name}' already registered and will be overwritten!"
            )
        self.commands[cmd.name] = cmd

        for alias in cmd.aliases:
            self.commands_aliases[alias] = cmd

    def unregister(self, command: Command) -> None:
        if command.name in self.commands:
            del self.commands[command.name]
            for alias in command.aliases:
                del self.commands_aliases[alias]
        else:
            raise KeyError(f"Command '{command.name}' not found in registry.")

    def reload_commands(self) -> None:
        """Reloads all loaded command plugins."""
        for cmd_name in self.commands:
            cmd = self.commands[cmd_name]
            module = self._import_module(cmd.__module__)
            reloaded_module = self._reload_module(module)
            if hasattr(reloaded_module, "register"):
                reloaded_module.register(self)

    def get_command(self, name: str) -> Command | None:
        if name in self.commands:
            return self.commands[name]

        if name in self.commands_aliases:
            return self.commands_aliases[name]

    def get_command_by_alias(self, alias: str) -> Command | None:
        return self.commands_aliases.get(alias)

    def reload_command(self, command: Command) -> None:
        if command.name in self.commands:
            module = self._import_module(command.__module__)
            reloaded_module = self._reload_module(module)
            if hasattr(reloaded_module, "register"):
                reloaded_module.register(self)

    def load_commands_from_directory(self, directory: str) -> None:
        """Loads commands from a directory."""
        for module_name in importlib.util.find_spec(directory).submodule_names:
            self.import_command_module(f"{directory}.{module_name}")

    def load_commands_from_module(self, module_name: str) -> None:
        """Loads commands from a module."""
        self.import_command_module(module_name)

    def register_command(self, command_class: Type[Command]) -> Callable:
        """Registers a command class."""

        def decorator(func: Command) -> Command:
            cmd = func()
            cmd.__module__ = command_class.__module__
            cmd.__qualname__ = f"{command_class.__name__}.{func.__name__}"
            cmd.__class__ = command_class
            self.register(cmd)
            return cmd

        return decorator

    def unregister_command(self, command: Command) -> None:
        if command.name in self.commands:
            del self.commands[command.name]
            for alias in command.aliases:
                del self.commands_aliases[alias]
        else:
            raise KeyError(f"Command
