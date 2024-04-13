import glob
import math
import os
import subprocess
import sys
from abc import ABC
from pathlib import Path
from typing import Dict, List, Any

from agbenchmark.__main__ import OPTIONAL_CATEGORIES, TEMP_FOLDER_ABS_PATH
from agbenchmark.agent_api_interface import run_api_agent
from agbenchmark.utils.data_types import ChallengeData, Ground
from agbenchmark.utils.prompts import (
    END_PROMPT,
    FEW_SHOT_EXAMPLES,
    PROMPT_MAP,
    SCORING_MAP,
)
from agbenchmark.utils.utils import agent_eligibible_for_optional_categories

class Challenge(ABC):
    """The parent class to all specific challenges classes.
    Defines helper methods for running a challenge"""

    CHALLENGE_LOCATION: str = ""
    scores: Dict[str, Any] = {}  # this is for suites
    _data_cache: Dict[str, ChallengeData] = {}

    def __init_subclass__(cls) -> None:
        cls._data_cache = {}

    @property
    def data(self) -> ChallengeData:
        if self.CHALLENGE_LOCATION not in self._data_cache:
            self._data_cache[self.CHALLENGE_LOCATION] = ChallengeData.deserialize(
                self.CHALLENGE_LOCATION
            )
        return self._data_cache[self.CHALLENGE_LOCATION]

    @property
    def task(self) -> str:
        return self.data.task

    @property
    def dependencies(self) -> List[str]:
        return self.data.dependencies

    async def setup_challenge(self, config: Dict[str, Any], cutoff: int) -> None:
        # ...

    def test_method(self, config: Dict[str, Any]) -> None:
        raise NotImplementedError

    def get_artifacts_out(
        self, workspace: str | dict[str, str], ground: Ground
    ) -> List[str]:
        # ...

    def scoring(self, config: Dict[str, Any], content: str, ground: Ground) -> float:
        # ...

    def llm_eval(self, config: Dict[str, Any], content: str, ground: Ground) -> float:
        # ...

    def get_scores(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # ...

    def get_dummy_scores(self, test_name: str, scores: Dict[str, Any]) -> int | None:
        # ...

    def skip_optional_categories(self, config: Dict[str, Any]) -> None:
        # ...

    def __repr__(self) -> str:
        return f"Challenge(CHALLENGE_LOCATION='{self.CHALLENGE_LOCATION}', scores={self.scores})"
