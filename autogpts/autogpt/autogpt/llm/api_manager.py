from typing import List, Optional

import logging
from openai import Model, model_names
from openai.error import APIError

from autogpt.core.resource.model_providers.schema import ChatModelInfo
from autogpt.singleton import Singleton

logger = logging.getLogger(__name__)


class ApiManager(metaclass=Singleton):
    def __init__(self):
        self.total_prompt_tokens: int = 0
        self.total_completion_tokens: int = 0
        self.total_cost: float = 0
        self.total_budget: float = 0
        self.models: Optional[List[str]] = None

    def reset(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0
        self.models = None

    def update_cost(self, prompt_tokens: int, completion_tokens: int, model: str):
        # the .model property in API responses can contain version suffixes like -v2
        model = model[:-3] if model.endswith("-v2") else model
        model_info = OPEN_AI_MODELS.get(model, None)

        if model_info is None:
            logger.warning(f"Unknown model: {model}")
            return

        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens

        self.total_cost += (
            prompt_tokens * model_info.prompt_token_cost / 1000
            + completion_tokens * model_info.completion_token_cost / 1000
        )

        logger.debug(f"Total running cost: ${self.total_cost:.3f}")

    def set_total_budget(self, total_budget: float):
        if total_budget < 0:
            raise ValueError("Total budget should be a non-negative value.")
        self.total_budget = total_budget

    def get_total_prompt_tokens(self) -> int:
        return self.total_prompt_tokens

    def get_total_completion_tokens(self) -> int:
        return self.total_completion_tokens

    def get_total_cost(self) -> float:
        return self.total_cost

    def get_total_budget(self) -> float:
        return self.total_budget

    @property
    def remaining_budget(self) -> float:
        return self.total_budget - self.total_cost

    def get_models(self, **openai_credentials) -> List[str]:
        if self.models is None:
            try:
                self.models = model_names(**openai_credentials)
            except APIError as e:
                logger.warning(f"Failed to fetch models: {e}")
                self.models = []

        return self.models
