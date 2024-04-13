import abc
import logging
import asyncio
from typing import Any
from pathlib import Path

class AbstractAgent(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    @abc.abstractmethod
    async def from_workspace(
        cls,
        workspace_path: Path,
        logger: logging.Logger,
    ) -> "AbstractAgent":
        ...

    @abc.abstractmethod
    async def determine_next_ability(self, *args, **kwargs) -> Any:
        ...

    @abc.abstractmethod
    def __repr__(self) -> str:
        ...


class Agent(AbstractAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ...

    @classmethod
    async def from_workspace(
        cls,
        workspace_path: Path,
        logger: logging.Logger,
    ) -> "Agent":
        ...

    async def determine_next_ability(self, *args, **kwargs) -> Any:
        ...

