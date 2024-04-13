import json
from dataclasses import dataclass
from typing import Any, Optional, Union

@dataclass
class StepRequestBody:
    """
    Body of the task request.
    """

    input: Optional[str] = None
    additional_input: Optional[Union[str, int, float, bool, dict, list]] = None

    def to_json(self) -> str:
        """Returns the JSON representation of the model"""
        return json.dumps(self, default=str)


