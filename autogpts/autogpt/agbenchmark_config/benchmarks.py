import asyncio
import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import autogpt
from autogpt.agents.agent import Agent, AgentConfiguration, AgentSettings
from autogpt.app.main import _configure_openai_provider, run_interaction_loop
from autogpt.commands import COMMAND_CATEGORIES
from autogpt.config import AIProfile, ConfigBuilder
from autogpt.config.logs import configure_logging
from autogpt.models.command_registry import CommandRegistry

LOG_DIR = Path(__file__).parent / "logs"


def build_config() -> autogpt.Config:
    config = ConfigBuilder.build_config_from_env()
    config.logging.level = logging.DEBUG
    config.logging.log_dir = LOG_DIR
    config.logging.plain_console_output = True
    configure_logging(**config.logging.dict())
    return config


async def run_agent(task: str, continuous_mode: bool = False) -> None:
    config = build_config()
    command_registry = CommandRegistry.with_command_modules(COMMAND_CATEGORIES, config)

    ai_profile = AIProfile(
        ai_name="AutoGPT",
        ai_role="a multi-purpose AI assistant.",
        ai_goals=[task],
    )

    agent_settings = AgentSettings(
        name=Agent.default_settings.name,
        description=Agent.default_settings.description,
        ai_profile=ai_profile,
        config=AgentConfiguration(
            fast_llm=config.fast_llm,
            smart_llm=config.smart_llm,
            allow_fs_access=not config.restrict_to_workspace,
            use_functions_api=config.openai_functions,
            plugins=config.plugins,
        ),
        prompt_config=Agent.default_settings.prompt_config.copy(deep=True),
        history=Agent.default_settings.history.copy(deep=True),
    )

    agent = Agent(
        settings=agent_settings,
        llm_provider=_configure_openai_provider(config),
        command_registry=command_registry,
        legacy_config=config,
    )
    agent.attach_fs(config.app_data_dir / "agents" / "AutoGPT-benchmark")  # HACK
    await run_interaction_loop(agent, continuous_mode=continuous_mode)


def run_specific_agent(task: str, continuous_mode: bool = False) -> None:
    try:
        asyncio.run(run_agent(task, continuous_mode))
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a specific Auto-GPT agent")
    parser.add_argument("task", help="The task for the agent to perform")
    args = parser.parse_args()

    run_specific_agent(args.task, continuous_mode=True)
