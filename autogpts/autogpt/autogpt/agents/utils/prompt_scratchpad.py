import logging
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pydantic
from pydantic import BaseModel
from pydantic import Field

from autogpt.core.resource.model_providers.schema import CompletionModelFunction
from autogpt.core.utils.json_schema import JSONSchema

logger = logging.getLogger("PromptScratchpad")


class JSONSchemaType(str, Enum):
    STRING = "string"
    OBJECT = "object"
    ARRAY = "array"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"


@dataclass
class CallableCompletionModelFunction(CompletionModelFunction):
    method: Callable


class PromptScratchpad(BaseModel):
    commands: Dict[str, CallableCompletionModelFunction] = Field(default_factory=dict)
    resources: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    best_practices: List[str] = Field(default_factory=list)

    def add_constraint(self, constraint: str) -> None:
        if constraint not in self.constraints:
            self.constraints.append(constraint)

    def add_command(
        self,
        name: str,
        description: str,
        params: Dict[str, Optional[Dict[str, Any]]],
        function: Callable,
    ) -> None:
        for param_name, param_spec in params.items():
            if not self._is_valid_param_spec(param_spec):
                logger.warning(
                    f"Cannot add command '{name}': "
                    f"parameter '{param_name}' has an invalid type specification."
                )
                return

        command = CallableCompletionModelFunction(
            name=name,
            description=description,
            parameters={
                param_name: JSONSchema(
                    type=self._json_schema_type_to_value(param_spec["type"])
                    if "type" in param_spec
                    else JSONSchemaType.STRING
                ).dict()
                if param_spec is not None
                else None
                for param_name, param_spec in params.items()
            },
            method=function,
        )

        if name in self.commands:
            if description == self.commands[name].description:
                return
            logger.warning(
                f"Replacing command {self.commands[name]} with conflicting {command}"
            )
        self.commands[name] = command

    def add_resource(self, resource: str) -> None:
        if resource not in self.resources:
            self.resources.append(resource)

    def add_best_practice(self, best_practice: str) -> None:
        if best_practice not in self.best_practices:
            self.best_practices.append(best_practice)

    @staticmethod
    def _json_schema_type_to_value(json_schema_type: JSONSchemaType) -> str:
        return json_schema_type.value

    @staticmethod
    def _is_valid_param_spec(param_spec: Optional[Dict[str, Any]]) -> bool:
        if param_spec is None:
            return True

        valid_types = [t.value for t in JSONSchemaType]
        return (
            "type" in param_spec
            and isinstance(param_spec["type"], str)
            and param_spec["type"] in valid_types
        )
