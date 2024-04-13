import os
import random
import string
import tempfile
from pathlib import Path
from typing import Any, Callable, Generator, List, Optional

import pytest
from _pytest.fixtures import FixtureRequest

import autogpt.commands.execute_code as sut  # system under testing
from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import (
    InvalidArgumentError,
    OperationNotAllowedError,
)


@pytest.fixture
def random_string(request: FixtureRequest) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10))


@pytest.fixture
def random_code(random_string: str) -> str:
    return f"print('Hello {random_string}!')"


@pytest.fixture
def python_test_file(
    agent: Agent, random_code: str, tmp_path: Path
) -> Generator[Path, None, None]:
    test_file = tmp_path / "test_file.py"
    test_file.write_text(random_code)

    yield test_file


@pytest.fixture
def python_test_args_file(agent: Agent, tmp_path: Path) -> Path:
    test_file = tmp_path / "test_args_file.py"
    test_file.write_text("import sys\nprint(sys.argv[1], sys.argv[2])")

    return test_file


@pytest.fixture
def python_test_args(random_string: str) -> List[str]:
    return [random_string, random_string]


def test_execute_python_file(
    python_test_file: Path, random_string: str, agent: Agent
) -> None:
    result: str = sut.execute_python_file(python_test_file, agent=agent)
    assert result.replace("\r", "") == f"Hello {random_string}!\n"


def test_execute_python_file_args(
    python_test_args_file: Path, python_test_args: List[str], agent: Agent
) -> None:
    result = sut.execute_python_file(
        python_test_args_file, args=python_test_args, agent=agent
    )
    assert result == f"{python_test_args[0]} {python_test_args[1]}\n"


def test_execute_python_code(random_code: str, random_string: str, agent: Agent) -> None:
    result: str = sut.execute_python_code(random_code, agent=agent)
    assert result.replace("\r", "") == f"Hello {random_string}!\n"


def test_execute_python_file_invalid(agent: Agent) -> None:
    with pytest.raises(InvalidArgumentError):
        sut.execute_python_file(Path("not_python.txt"), agent)


def test_execute_python_file_not_found(agent: Agent) -> None:
    with pytest.raises(
        FileNotFoundError,
        match=r"python: can't open file '([a-zA-Z]:)?[/\\\-\w]*notexist.py': "
        r"\[Errno 2\] No such file or directory",
    ):
        sut.execute_python_file(Path("notexist.py"), agent)


@pytest.mark.parametrize(
    "command, expected_result",
    [
        ("echo 'Hello World!'", "Hello World!\n"),
        ("echo 'Hello {}'".format(random_string), f"Hello {random_string}\n"),
    ],
)
def test_execute_shell(
    command: str, expected_result: str, agent: Agent, tmp_path: Path, capfd: Any
) -> None:
    with capfd.disabled():
        result = sut.execute_shell(command, agent, cwd=tmp_path)
        assert expected_result in result.out


def test_execute_shell_local_commands_not_allowed(
    agent: Agent, tmp_path: Path, capfd: Any
) -> None:
    with capfd.disabled():
        result = sut.execute_shell("pwd", agent, cwd=tmp_path)
        assert "Local commands are not allowed" in result.err


def test_execute_shell_denylist_should_deny(
    agent: Agent, random_string: str, tmp_path: Path, capfd: Any
) -> None:
    agent.legacy_config.shell_denylist = ["echo"]

    with capfd.disabled():
        with pytest.raises(OperationNotAllowedError, match="not allowed"):
            sut.execute_shell("echo 'Hello {}'".format(random_string), agent, cwd=tmp_path)


def test_execute_shell_denylist_should_allow(
    agent: Agent, random_string: str, tmp_path: Path, capfd: Any
) -> None:
    agent.legacy_config.shell_denylist = ["cat"]

    with capfd.disabled():
        result = sut.execute_shell("echo 'Hello {}'".format(random_string), agent, cwd=tmp_path)
        assert "Hello" in result.out and random_string in result.out


def test_execute_shell_allowlist_should_deny(
    agent: Agent, random_string: str, tmp_path: Path, capfd: Any
) -> None:
    agent.legacy_config.shell_command_control = sut.ALLOWLIST_CONTROL
    agent.legacy_config.shell_allowlist = ["cat"]

    with capfd.disabled():
        with pytest.raises(OperationNotAllowedError, match="not allowed"):
            sut.execute_shell("echo 'Hello {}'".format(random_string), agent, cwd=tmp_path)


def test_execute_shell_allowlist
