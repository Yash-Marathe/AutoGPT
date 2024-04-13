import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

from autogpt.core.configuration import Configurable, SystemConfiguration, SystemSettings
from autogpt.core.memory.base import Memory
from autogpt.core.workspace import Workspace
from typing_extensions import TypedDict


class MemoryConfiguration(SystemConfiguration):
    pass


class MemorySettings(SystemSettings):
    configuration: MemoryConfiguration


class MessageHistory:
    def __init__(self, previous_message_history: List[str]):
        self._message_history = previous_message_history

    def append(self, message: str):
        self._message_history.append(message)


class SimpleMemory(Memory, Configurable):
    default_settings = MemorySettings(
        name="simple_memory",
        description="A simple memory.",
        configuration=MemoryConfiguration(),
    )

    def __init__(
        self,
        settings: MemorySettings,
        logger: logging.Logger,
        workspace: Workspace,
    ):
        super().__init__(settings=settings, logger=logger)
        self._workspace = workspace
        self._message_history_path = self._workspace.get_path("message_history.json")
       
