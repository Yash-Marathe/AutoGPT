from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture

from autogpt.core.resource.model_providers import (
    OPEN_AI_CHAT_MODELS,
    OPEN_AI_EMBEDDING_MODELS,
)
from autogpt.llm.api_manager import ApiManager

@pytest.fixture(autouse=True)
def api_manager_instance():
    api_manager = ApiManager()
    api_manager.reset()
    yield api_manager


@pytest.fixture(autouse=True)
def mock_costs(mocker: MockerFixture, api_manager_instance):
    mocker.patch.multiple(
        OPEN_AI_CHAT_MODELS["gpt-3.5-turbo"],
        prompt_token_cost=0.0013,
        completion_token_cost=0.0025,
    )
    mocker.patch.multiple(
        OPEN_AI_EMBEDDING_MODELS["text-embedding-ada-002"],
        prompt_token_cost=0.0004,
    )

    api_manager_instance.update_cost(600, 1200, "gpt-3.5-turbo")
    api_manager_instance.set_total_budget(10.0)


class TestApiManager:
    @pytest.mark.usefixtures("api_manager_instance")
    def test_getter_methods(self, api_manager_instance):
        """Test the getter methods for total tokens, cost, and budget."""
        assert api_manager_instance.get_total_prompt_tokens() == 600
        assert api_manager_instance.get_total_completion_tokens() == 1200
        assert api_manager_instance.get_total_cost() == (600 * 0.0013 + 1200 * 0.0025) / 1000
        assert api_manager_instance.get_total_budget() == 10.0

    @staticmethod
    def test_set_total_budget(api_manager_instance):
        """Test if setting the total budget works correctly."""
        total_budget = 15.0
        api_manager_instance.set_total_budget(total_budget)

        assert api_manager_instance.get_total_budget() == total_budget

    @staticmethod
    def test_update_cost_completion_model(api_manager_instance):
        """Test if updating the cost works correctly."""
        prompt_tokens = 70
        completion_tokens = 140
        model = "gpt-3.5-turbo"

        api_manager_instance.update_cost(prompt_tokens, completion_tokens, model)

        assert api_manager_instance.get_total_prompt_tokens() == prompt_tokens
        assert api_manager_instance.get_total_completion_tokens() == completion_tokens
        assert (
            api_manager_instance.get_total_cost()
            == (prompt_tokens * 0.0013 + completion_tokens * 0.0025) / 1000
        )

    @staticmethod
    def test_update_cost_embedding_model(api_manager_instance):
        """Test if updating the cost works correctly."""
        prompt_tokens = 1500
        model = "text-embedding-ada-002"

        api_manager_instance.update_cost(prompt_tokens, 0, model)

        assert api_manager_instance.get_total_prompt_tokens() == prompt_tokens
        assert api_manager_instance.get_total_completion_tokens() == 0
        assert api_manager_instance.get_total_cost() == (prompt_tokens * 0.0004) / 1000

    @staticmethod
    def test_get_models(api_manager_instance):
        """Test if getting models works correctly."""
        with patch("openai.Model.list") as mock_list_models:
            mock_list_models.return_value = {"data": [{"id": "gpt-3.5-turbo"}]}
            result = api_manager_instance.get_models()

            assert result[0]["id"] == "gpt-3.5-turbo"
            assert api_manager_instance.models[0]["id"] == "gpt-3.5-turbo"
