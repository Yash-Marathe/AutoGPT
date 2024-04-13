import dataclasses
from typing import Optional

from autogpt.core.utils.json_schema import JSONSchema


@dataclasses.dataclass
class CommandParameter:
    name: str
    spec: JSONSchema
    description: Optional[str] = None
    required: Optional[bool] = None

    def __post_init__(self):
        if self.description is None:
            self.description = self.spec.description
        if self.required is None:
            self.required = self.spec.required

    def __repr__(self):
        return (
            f"CommandParameter({self.name!r}, {self.spec.type!r}, "
            f"{self.description!r}, {self.required!r})"
        )
