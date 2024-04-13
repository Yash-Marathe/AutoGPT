import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, Final, List, Literal, NamedTuple, TypeVar

import autogpt.core.ability.base  # type: ignore
from autogpt.core.ability.schema import AbilityResult  # type: ignore
from autogpt.core.memory.base import Memory  # type: ignore
from autogpt.core.plugin.simple import SimplePluginService  # type: ignore
from autogpt.core.resource.model_providers import (
    ChatModelProvider,
    CompletionModelFunction,
    ModelProviderName,
)  # type: ignore
from autogpt.core.workspace.base import Workspace  # type: ignore
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autogpt.core.ability.base import Ability
    from autogpt.core.configuration import Configurable, SystemConfiguration, SystemSettings
    from autogpt.core.resource.model_providers import ChatModelProvider

