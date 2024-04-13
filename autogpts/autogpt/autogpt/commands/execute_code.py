import logging
import os
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, List, Optional

import docker
from docker.errors import DockerException, ImageNotFound, NotFound
from docker.types import Mount
from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import (
    CodeExecutionError,
    CommandExecutionError,
    InvalidArgumentError,
    OperationNotAllowedError,
)
from autogpt.command_decorator import command
from autogpt.config import Config
from autogpt.core.utils.json_schema import JSONSchema

from .decorators import sanitize_path_arg

COMMAND_CATEGORY = "execute_code"
COMMAND_CATEGORY_TITLE = "Execute Code"

logger = logging.getLogger(__name__)

ALLOWLIST_CONTROL = "allowlist"
DENYLIST_CONTROL = "denylist"


def is_valid_file_path(file_path: Path, agent: Agent) -> bool:
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")
    if not file_path.is_file():
        raise InvalidArgumentError(f"Invalid file path '{file_path}'")
    if not str(file_path).endswith(".py"):
        raise InvalidArgumentError("Only .py files are allowed")
    if not file_path.relative_to(agent.workspace.root).is_absolute():
        raise InvalidArgumentError("File path must be within the workspace")
    return True


def is_valid_command(command: str, config: Config) -> bool:
    if not command:
        return False

    command_name = command.split()[0]

    if config.shell_command_control == ALLOWLIST_CONTROL:
        return command_name in config.shell_allowlist
    else:
        return command_name not in config.shell_denylist


@command(
    "execute_python_code",
    "Executes the given Python code inside a single-use Docker container"
    " with access to your workspace folder",
    {
        "code": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The Python code to run",
            required=True,
        ),
    },
)
def execute_python_code(code: str, agent: Agent) -> str:
    """
    Create and execute a Python file in a Docker container and return the STDOUT of the
    executed code.

    If the code generates any data that needs to be captured, use a print statement.

    Args:
        code (str): The Python code to run.
        agent (Agent): The Agent executing the command.

    Returns:
        str: The STDOUT captured from the code when it ran.
    """

    tmp_code_file = NamedTemporaryFile(
        "w", dir=agent.workspace.root, suffix=".py", encoding="utf-8"
    )
    tmp_code_file.write(code)
    tmp_code_file.flush()

    try:
        return execute_python_file(tmp_code_file.name, agent)
    except Exception as e:
        raise CommandExecutionError(*e.args)
    finally:
        tmp_code_file.close()


@command(
    "execute_python_file",
    "Execute an existing Python file inside a single-use Docker container"
    " with access to your workspace folder",
    {
        "filename": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The name of the file to execute",
            required=True,
        ),
        "args": JSONSchema(
            type=JSONSchema.Type.ARRAY,
            description="The (command line) arguments to pass to the script",
            required=False,
            items=JSONSchema(type=JSONSchema.Type.STRING),
        ),
    },
)
@sanitize_path_arg("filename")
def execute_python_file(
    filename: Path, agent: Agent, args: List[str] = []
) -> str:
    """Execute a Python file in a Docker container and return the output

    Args:
        filename (Path): The name of the file to execute
        agent (Agent): The Agent executing the command
        args (List[str], optional): The arguments with which to run the python script

    Returns:
        str: The output of the file
    """
    logger.info(
        f"Executing python file '{filename}' "
        f"in working directory '{agent.workspace.root}'"
    )

    is_valid_file_path(filename, agent)

    if isinstance(args, str):
        args = args.split()  # Convert space-separated string to a list

    file_path = filename

    if we_are_running_in_a_docker_container():
        logger.debug(
            "AutoGPT is running in a Docker container; "
            f"executing {file_path} directly..."
        )
        result = subprocess.run(
           
