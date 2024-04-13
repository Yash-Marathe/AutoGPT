from __future__ import annotations
from typing import List, Any

from autogpt.core.prompting import ChatPrompt, ChatMessage
from autogpt.models.context_item import ContextItem
from autogpt.agents.base import BaseAgent

class AgentContext:
    """Context container for an agent"""

    def __init__(self, items: List[ContextItem] = None):
        """Initialize the AgentContext object

        Args:
            items (List[ContextItem], optional): Initial context items. Defaults to None.
        """
        self.items = items or []

    def __bool__(self) -> bool:
        return bool(self.items)

    def __contains__(self, item: ContextItem) -> bool:
        return any(i.source == item.source for i in self.items)

    def add(self, item: ContextItem) -> None:
        """Add a context item to the list

        Args:
            item (ContextItem): The context item to add
        """
        self.items.append(item)

    def close(self, index: int) -> None:
        """Remove a context item from the list

        Args:
            index (int): The index of the context item to remove
        """
        self.items.pop(index - 1)

    def clear(self) -> None:
        """Clear all context items from the list"""
        self.items.clear()

    def format_numbered(self) -> str:
        """Format the context items as a numbered list

        Returns:
            str: The formatted context items
        """
        return "\n\n".join([f"{i}. {c.fmt()}" for i, c in enumerate(self.items, 1)])


class ContextMixin:
    """Mixin that adds context support to a BaseAgent subclass"""

    context: AgentContext

    def __init__(self, **kwargs: Any):
        """Initialize the ContextMixin object

        Args:
            **kwargs: Additional keyword arguments
        """
        self.context = AgentContext()
        super().__init__(**kwargs)

    def build_prompt(
        self,
        *args: Any,
        extra_messages: List[ChatMessage] = None,
        **kwargs: Any,
    ) -> ChatPrompt:
        """Build a chat prompt with the context section included

        Args:
            *args: Variable length argument list
            extra_messages (List[ChatMessage], optional): Additional messages to include in the prompt. Defaults to None.
            **kwargs: Additional keyword arguments

        Returns:
            ChatPrompt: The chat prompt with the context section included
        """
        if extra_messages is None:
            extra_messages = []

        if self.context:
            extra_messages.insert(
                0,
                ChatMessage.system(
                    "## Context\n"
                    f"{self.context.format_numbered()}\n\n"
                    "When a context item is no longer needed and you are not done yet, "
                    "you can hide
