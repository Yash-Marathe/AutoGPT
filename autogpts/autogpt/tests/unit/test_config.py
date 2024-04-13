import os
from typing import Any

import pytest
from pydantic import SecretStr
from unittest.mock import patch

import autogpt.app.configurator
from autogpt.config import Config, ConfigBuilder


@pytest.fixture(scope="module")
def config() -> Config:
    return ConfigBuilder.build_config()


def test_initial_values(config: Config) -> None:
    """Test if the initial values of the config class attributes are set correctly."""
    assert not config.continuous_mode
    assert not config.tts_config.speak_mode
    assert config.fast_llm == "gpt-3.5-turbo-16k"
    assert config.smart_llm.startswith("gpt-4")


@pytest.mark.parametrize(
    "new_value,expected_value",
    [
        (True, True),
        (False, False),
    ],
)
def test_set_continuous_mode(config: Config, new_value: bool, expected_value: bool) -> None:
    """Test if the set_continuous_mode() method updates the continuous_mode attribute."""
    original_value = config.continuous_mode
    config.continuous_mode = new_value
    assert config.continuous_mode == expected_value
    config.continuous_mode = original_value


@pytest.mark.parametrize(
    "new_value,expected_value",
    [
        (True, True),
        (False, False),
    ],
)
def test_set_speak_mode(config: Config, new_value: bool, expected_value: bool) -> None:
    """Test if the set_speak_mode() method updates the speak_mode attribute."""
    original_value = config.tts_config.speak_mode
    config.tts_config.speak_mode = new_value
    assert config.tts_config.speak_mode == expected_value
    config.tts_config.speak_mode = original_value


@pytest.mark.parametrize(
    "new_value,expected_value",
    [
        ("gpt-3.5-turbo-test", "gpt-3.5-turbo-test"),
        ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k"),
    ],
)
def test_set_fast_llm(config: Config, new_value: str, expected_value: str) -> None:
    """Test if the set_fast_llm() method updates the fast_llm attribute."""
    original_value = config.fast_llm
    config.fast_llm = new_value
    assert config.fast_llm == expected_value
    config.fast_llm = original_value


@pytest.mark.parametrize(
    "new_value,expected_value",
    [
        ("gpt-4-test", "gpt-4-test"),
        ("gpt-4", "gpt-4"),
    ],
)
def test_set_smart_llm(config: Config, new_value: str, expected_value: str) -> None:
    """Test if the set_smart_llm() method updates the smart_llm attribute."""
    original_value = config.smart_llm
    config.smart_llm = new_value
    assert config.smart_llm == expected_value
    config.smart_llm = original_value


@patch("autogpt.app.configurator.Model.list")
def test_smart_and_fast_llms_set_to_gpt4(
    mock_list_models: Any, config: Config
) -> None:
    """Test if models update to gpt-3.5-turbo if gpt-4 is not available."""
    original_fast_llm = config.fast_llm
    original_smart_llm = config.smart_llm

    config.fast_llm = "gpt-4"
    config.smart_llm = "gpt-4"

    mock_list_models.return_value = {"data": [{"id": "gpt-3.5-turbo"}]}

    autogpt.app.configurator.apply_overrides_to_config(
        config=config,
        gpt3only=False,
        gpt4only=False,
    )

    assert config.fast_llm == "gpt-3.5-turbo"
    assert config.smart_llm == "gpt-3.5-turbo"

    # Reset config
    config.fast_llm = original_fast_llm
    config.smart_llm = original_smart_llm


def test_missing_azure_config(config: Config) -> None:
    """Test missing Azure configuration."""
    assert config.openai_credentials is not None

    config_file = config.app_data_dir / "azure_config.yaml"

    with pytest.raises(FileNotFoundError):
        config.openai_credentials.load_azure_config(config_file)

    config_file.write
