from typing import Any, List

def format_numbered_list(items: List[Any], start_at: int = 1) -> str:
    """Format a list of items as a numbered list, starting at the given index."""
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start_at))

def indent(content: str, indentation: int | str = 4) -> str:
    """Indent the given content by the specified amount."""
    if isinstance(indentation, int):
        indentation = " " * indentation
    return "".join([indentation, *content.splitlines(), ""])
