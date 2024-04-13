from typing import TYPE_CHECKING, AsyncContextManager

if TYPE_CHECKING:
    from autogpt.agents.agent import Agent
    from autogpt.config import Config
    from autogpt.core.resource.model_providers.schema import ChatModelProvider
    from autogpt.ai_directives import AIDirectives
    from autogpt.configurators import _configure_agent
    from autogpt.profile_generator import generate_agent_profile_for_task

