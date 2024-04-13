import os
import pytest
from sqlite3 import Connection
from typing import AsyncContextManager

import pytest_asyncio
from forge.sdk.db import AgentDB
from forge.sdk.db.models import TaskModel, StepModel, ArtifactModel

@pytest.fixture
def agent_db() -> AsyncContextManager[AgentDB]:
    db_name = "test_db.sqlite3"
    agent_db = AgentDB(db_name)
    yield agent_db
    os.remove(Path(db_name).absolute())

@pytest.fixture
def connection() -> AsyncContextManager[Connection]:
    db_name = "test_db.sqlite3"
    conn = sqlite3.connect(db_name)
    yield conn
    conn.close()
    os.remove(Path(db_name).absolute())

@pytest.fixture
def task(agent_db: AgentDB) -> TaskModel:
    return agent_db.create_task("test_input")

@pytest.fixture
def step(agent_db: AgentDB, task: TaskModel) -> StepModel:
    step_input = StepInput(type="python/code")
    request = StepRequestBody(input="test_input debug", additional_input=step_input)
    return agent_db.create_step(task.task_id, request)

@pytest.fixture
def artifact(agent_db: AgentDB, task: TaskModel, step: StepModel) -> ArtifactModel:
    return agent_db.create_artifact(
        task_id=task.task_id,
        file_name="test_get_artifact_sample_file.txt",
        relative_path="file:///path/to/test_get_artifact_sample_file.txt",
        agent_created=True,
        step_id=step.step_id,
    )


import pytest
from datetime import datetime
from pathlib import Path
from typing import Any

from forge.sdk.db import AgentDB
from forge.sdk.db.models import TaskModel, StepModel, ArtifactModel
from forge.sdk.errors import NotFoundError as DataNotFoundError
from forge.sdk.db.converters import convert_to_task, convert_to_step, convert_to_artifact

pytestmark = [pytest.mark.asyncio]

def test_table_creation(connection: Connection):
    cursor = connection.cursor()

    # Test for tasks table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    assert cursor.fetchone() is not None

    # Test for steps table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='steps'")
    assert cursor.fetchone() is not None

    # Test for artifacts table existence
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts'"
    )
    assert cursor.fetchone() is not None

@pytest.mark.asyncio
async def test_task_schema(task: TaskModel) -> None:
    assert task.task_id == "test_input"
    assert task.input == "test_input"
    assert len(task.artifacts) == 0

@pytest.mark.asyncio
async def test_step_schema(step: StepModel) -> None:
    assert step.task_id == "test_input"
    assert step.step_id == "test_input"
    assert step.name == "test_input"
    assert step.status == "created"
    assert step.output == "test_input"
    assert len(step.artifacts) == 0
    assert step.is_last is False

@pytest.mark.asyncio
async def test_convert_to_task(task: TaskModel) -> None:
    converted_task = convert_to_task(task)
    assert converted_task.task_id == "test_input"
    assert converted_task.input == "test_input"
    assert len(converted_task.artifacts) == 0

@pytest.mark.asyncio
async def test_convert_to_step(step: StepModel) -> None:
    converted_step = convert_to_step(step)
    assert converted_step.task_id == "test_input"
    assert converted_step.step_id == "test_input"
    assert converted_step.name == "test_input"
    assert converted_step.status == "created"
    assert converted_step.output == "test_input"
    assert len(converted_step.artifacts) == 0
    assert converted_step.is_last is False

@pytest.mark.asyncio
async def test_convert_to_artifact(artifact: ArtifactModel) -> None:
    converted_artifact = convert_to_artifact(artifact)
    assert converted_artifact.artifact_id == "test_input"
    assert converted_artifact.relative_path == "file:///path/to/test_get_artifact_sample_file.txt"
    assert converted_artifact.agent_created is True

@pytest.mark.asyncio
async def test_create_task(agent_db: AgentDB) -> None:
    task = await agent_db.create_task("test_input")
    assert task.input == "test_input"

@pytest.mark.asyncio
async def test_create_and_get_task(agent_db: AgentDB) -> None:
