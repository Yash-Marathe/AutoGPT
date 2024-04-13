"""Commands to perform Git operations"""

from pathlib import Path
from urllib.parse import urlparse
import git
import time
from typing import Any, Dict, Union

from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import CommandExecutionError
from autogpt.command_decorator import command
from autogpt.core.utils.json_schema import JSONSchema
from autogpt.url_utils.validators import validate_url

from .decorators import sanitize_path_arg

COMMAND_CATEGORY = "git_operations"
COMMAND_CATEGORY_TITLE = "Git Operations"

def is_git_repo_url(url: str) -> bool:
    """Check if the URL is a valid Git repository URL.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is a valid Git repository URL, False otherwise.
    """
    try:
        repo = git.Repo(url=url)
        return True
    except git.exc.GitError:
        return False

@command(
    "clone_repository",
    "Clones a Repository",
    {
        "url": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The URL of the repository to clone",
            required=True,
        ),
        "clone_path": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The path to clone the repository to",
            required=True,
        ),
        "timeout": JSONSchema(
            type=JSONSchema.Type.INTEGER,
            description="The timeout in seconds for the clone operation",
            required=False,
            default=300,
        ),
    },
    lambda config: bool(config.github_username and config.github_api_key),
    "Configure github_username and github_api_key.",
)
@sanitize_path_arg("clone_path")
@validate_url
def clone_repository(url: str, clone_path: Path, timeout: int, agent: Agent) -> str:
    """Clone a GitHub repository locally.

    Args:
        url (str): The URL of the repository to clone.
        clone_path (Path): The path to clone the repository to.
        timeout (int): The timeout in seconds for the clone operation.

    Returns:
        str: The result of the clone operation.
