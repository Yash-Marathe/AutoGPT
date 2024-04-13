from typing import Optional


class NotFoundError(Exception):
    pass


class AgentError(Exception):
    """Base class for specific exceptions relevant in the execution of Agents"""

    message: str
    hint: Optional[str] = None

    def __init__(self, message: str, hint: Optional[str] = None, *args):
        self.message = message
        self.hint = hint
        super().__init__(message, *args)


class ConfigurationError(AgentError):
    """Error caused by invalid, incompatible or otherwise incorrect configuration"""


class AgentResponseError(AgentError):
    """Error caused by issues with the Agent's response format"""


class InvalidCommandError(AgentResponseError):
    """The LLM deviated from the prescribed response format"""


class UnknownCommandError(AgentResponseError):
    """The AI tried to use an unknown command"""

    hint = "Do not try to use this command again."


class CommandExecutionError(AgentError):
    """Base class for errors caused by issues with command execution"""


class InvalidArgumentError(CommandExecutionError):
    """The command received an invalid argument"""


class DuplicateOperationError(CommandExecutionError):
    """The proposed operation has already been executed"""


class OperationNotAllowedError(CommandExecutionError):
    """The agent is not allowed to execute the proposed operation"""


class AccessDeniedError(CommandExecutionError):
    """The operation failed because access to a required resource was denied"""


class CodeExecutionError(CommandExecutionError):
    """The operation (an attempt to run arbitrary code) returned an error"""


class TooMuchOutputError(CommandExecutionError):
    """The operation generated more output than what the Agent can process"""
