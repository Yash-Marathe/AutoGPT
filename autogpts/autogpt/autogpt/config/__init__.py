"""
This module contains the configuration classes for AutoGPT.
"""

import sys

__version__ = "0.1.0"


def assert_config_has_openai_api_key(config: Config) -> None:
    """
    Assert that the given config object has an OpenAI API key set.

    Args:
        config (Config): The configuration object to check.

    Raises:
        ValueError: If the OpenAI API key is not set in the config.
    """
    if not config.openai_api_key:
        raise ValueError("OpenAI API key is not set in the config.")


class ConfigBuilder:
    """
    A builder class for creating Config objects.
    """

    def __init__(self):
        self.config = Config()

    def with_ai_profile(self, ai_profile: AIProfile) -> "ConfigBuilder":
        """
        Set the AI profile for the config.

        Args:
            ai_profile (AIProfile): The AI profile to use.

        Returns:
            ConfigBuilder: The builder instance for chaining.
        """
        self.config.ai_profile = ai_profile
        return self

    def with_ai_directives(self, ai_directives: AIDirectives) -> "ConfigBuilder":
        """
        Set the AI directives for the config.

        Args:
            ai_directives (AIDirectives): The AI directives to use.

        Returns:
            ConfigBuilder: The builder instance for chaining.
        """
        self.config.ai_directives = ai_directives
        return self

