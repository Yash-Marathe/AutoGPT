import abc
import enum
from typing import Any, Dict, List, Optional

import pydantic
from pydantic import BaseModel, SecretBytes, SecretField, SecretStr

from autogpt.core.configuration import (
    SystemConfiguration,
    SystemSettings,
    UserConfigurable,
)

class ResourceType(str, enum.Enum):
    """An enumeration of resource types."""

    MODEL = "model"
    MEMORY = "memory"

