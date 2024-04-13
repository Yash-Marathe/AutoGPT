import abc
from typing import Any, Awaitable, Dict, Generic, TypeVar

class LanguageModelResponse:
    def __init__(self, response: str):
        self.response = response

class Context:
    pass

class PlanningContext(Context):
    pass

class ReflectionContext(Context):
    pass

T = TypeVar('T')

class ResponsePromise(Generic[T]):
    def __init__(self, coroutine: Awaitable[T]):
        self.coroutine = coroutine

