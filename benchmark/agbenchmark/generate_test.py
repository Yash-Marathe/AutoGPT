import glob
import importlib
import json
import os
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pytest
from helicone.lock import HeliconeLockManager

from agbenchmark.agent_api_interface import append_updates_file
from agbenchmark.agent_protocol_client.models.step import Step
from agbenchmark.utils.challenge import Challenge
from agbenchmark.utils.data_types import AgentBenchmarkConfig, ChallengeData

DATA_CATEGORY: dict[str, str] = {}


@pytest.fixture(scope="module")
def create_single_test(
    data: ChallengeData, challenge_location: str, file_datum: Optional[list[dict[str, Any]]] = None
) -> type[Challenge]:
    challenge_data = None
    artifacts_location = None
    if isinstance(data, ChallengeData):
        challenge_data = data
        data = data.get_data()

    DATA_CATEGORY[data["name"]] = data["category"][0]

    # Define test class dynamically
    challenge_class = types.new_class(f"Test{data['name']}", (Challenge,))

    setattr(challenge_class, "CHALLENGE_LOCATION", challenge_location)

    setattr(
        challenge_class,
        "ARTIFACTS_LOCATION",
        artifacts_location or str(Path(challenge_location).resolve().parent),
    )

    # Define test method within the dynamically created class
    async def test_method(self, config: Dict[str, Any], request) -> None:  # type: ignore
        # create a random number between 0 and 1
        test_name = self.data.name

        try:
            with open(CHALLENGES_ALREADY_BEATEN, "r") as f:
                challenges_beaten_in_the_past = json.load(f)
        except:
            challenges_beaten_in_the_past = {}

        if request.config.getoption("--explore") and challenges_beaten_in_the_past.get(
            test_name, False
        ):
            return None

        # skip optional categories
        self.skip_optional_categories(config)

        if os.environ.get("HELICONE_API_KEY"):
            HeliconeLockManager.write_custom_property("challenge", self.data.name)

        cutoff = self.data.cutoff or 60

        timeout = cutoff
        if "--nc" in sys.argv:
            timeout = 100000
        if "--cutoff" in sys.argv:
            timeout = int(sys.argv[sys.argv.index("--cutoff") + 1])

        await self.setup_challenge(config, timeout)

        scores = self.get_scores(config)
        request.node.answers = (
            scores["answers"] if "--keep-answers" in sys.argv else None
        )
        del scores["answers"]  # remove answers from scores
        request.node.scores = scores  # store scores in request.node
        is_score_100 = 1 in scores["values"]

        evaluation = "Correct!" if is_score_100 else "Incorrect."
        eval_step = Step(
            input=evaluation,
            additional_input=None,
            task_id="irrelevant, this step is a hack",
            step_id="irrelevant, this step is a hack",
            name="",
            status="created",
            output=None,
            additional_output=None,
            artifacts=[],
            is_last=True,
        )
        await append_updates_file(eval_step)

        assert is_score_100

    # Parametrize the method here
    test_method = pytest.mark.parametrize(
        "challenge_data",
        [data],
        indirect=True,
    )(test_method)

    setattr(challenge_class, "test_method", test_method)

    return challenge_class


import json
from collections import deque
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from agbenchmark.agent_api_interface import CHALLENGES_ALREADY_BEATEN
from agbenchmark.utils.data_types import AgentBenchmarkConfig
from agbenchmark.utils.challenge import ChallengeData

# ... (keep the rest of the code the same)
