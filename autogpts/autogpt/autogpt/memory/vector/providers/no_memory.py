"""A class that does not store any data. This is the default memory provider."""
from __future__ import annotations

from typing import Iterator

from autogpt.config.config import Config
from ..memory_provider import VectorMemoryProvider
from ..memory_item import MemoryItem

class NoMemory(VectorMemoryProvider):
    """
    A class that does not store any data. This is the default memory provider.
    """

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)

    def __iter__(self) -> Iterator[MemoryItem]:
        return iter([])

    def __contains__(self, x: MemoryItem) -> bool:
        return False

    def __len__(self) -> int:
        return 0

    def add(self, item: MemoryItem):
        """
        Add a new memory item.
        This method does nothing in this implementation.
        """
        pass

    def discard(self, item: MemoryItem):
        """
        Discard a memory item.
        This method does nothing in this implementation.
        """
        pass

    def clear(self):
        """
        Clear all memory items.
        This method does nothing in this implementation.
        """
        pass
