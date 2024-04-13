import abc
from collections.abc import Callable
from typing import Any, ClassVar, List

import inflection
from pydantic import Field
from pydantic.main import BaseModel

from autogpt.core.configuration import SystemConfiguration
from autogpt.core.planning.simple import LanguageModelConfiguration
from autogpt.core.plugin.base import PluginLocation
from autogpt.core.resource.model_providers import CompletionModelFunction
from autogpt.core.utils.json_schema import JSONSchema

class AbilityResult(BaseModel):
    # Add any necessary fields or methods for AbilityResult here
    ...

class AbilityConfiguration(SystemConfiguration):
    """Struct for model configuration."""

    location: PluginLocation
    packages_required: List[str] = Field(default_factory=list)
    language_model_required: LanguageModelConfiguration = None
    memory_provider_required: bool = False
    workspace_required: bool = False

class AbstractAbility(abc.ABC):
    """A class representing an agent ability."""

    default_configuration: ClassVar[AbilityConfiguration]

    @classmethod
    def name(cls) -> str:
        """The name of the ability."""
        return inflection.underscore(cls.__name__)

    @property
    @classmethod
    @abc.abstractmethod
    def description(cls) -> str:
        """A detailed description of what the ability does."""
        ...

    @property
    @classmethod
    @abc.abstractmethod
    def parameters(cls) -> dict[str, JSONSchema]:
        ...

    @abc.abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> AbilityResult:
        ...

    def __str__(self) -> str:
        return str(self.spec)

    @property
    @classmethod
    def spec(cls) -> CompletionModelFunction:
        return CompletionModelFunction(
            name=cls.name(),
            description=cls.description,
            parameters=cls.parameters,
        )

class AbilityRegistry:
    """Registry for managing abilities."""

    def __init__(self):
        self._abilities = {}

    def register_ability(
        self, ability_name: str, ability_configuration: AbilityConfiguration
    ) -> None:
        if ability_name in self._abilities:
            raise ValueError(f"Ability with name {ability_name} already exists.")
        self._abilities[ability_name] = ability_configuration

    def list_abilities(self) -> List[str]:
        return list(self._abilities.keys())

    def dump_abilities(self) -> List[CompletionModelFunction]:
        return [ability.spec for ability in self._abilities.values()]

    def get_ability(self, ability_name: str) -> AbstractAbility:
        if ability_name not in self._abilities:
            raise ValueError(f"Ability with name {ability_name} not found.")
        # Instantiate the ability here and return it
        ...

    async def perform(self, ability_name: str, **kwargs: Any) -> AbilityResult:
        ability = self.get_ability(ability_name)
        return await ability(*kwargs.values())

