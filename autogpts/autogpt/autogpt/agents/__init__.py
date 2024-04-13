from .agent import Agent
from .base import AgentThoughts, CommandArgs, CommandName

"""Module for defining various agents and related classes."""

class BaseAgent(metaclass=AgentThoughts):
    """Base class for all agents with shared thoughts."""

class Agent(BaseAgent):
    """Class for defining an agent."""

class CommandName:
    """Class for defining command names."""

class CommandArgs:
    """Class for defining command arguments."""

__all__ = ["BaseAgent", "Agent", "CommandName", "CommandArgs"]
