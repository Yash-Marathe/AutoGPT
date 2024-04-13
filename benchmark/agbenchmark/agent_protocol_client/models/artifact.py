# coding: utf-8

from __future__ import annotations

import json
from typing import Optional

from pydantic import BaseModel

class Artifact(BaseModel):
    """
    Artifact that the task has produced.
    """

    artifact_id: str = Field(..., description="ID of the artifact.")
    file_name: str = Field(..., description="Filename of the artifact.")
    relative_path: Optional[str] = Field(
        None, description="Relative path of the artifact in the agent's workspace."
    )
    created_at: str = Field(..., description="Creation date of the artifact.")
    agent_created: bool = Field(..., description="True if created by the agent")

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_json(self) -> str:
        """Returns the JSON representation of the model"""
        return json.dumps(self.dict(), indent=4)

    @classmethod
    def from_json(cls, json_str: str) -> Artifact:
        """Create an instance of Artifact from a JSON string"""
        return cls.parse_raw(json_str)

