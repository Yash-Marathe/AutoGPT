import dataclasses
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Tuple
import uuid
from dataclasses import dataclass

@dataclass
class TaskModel:
    task_id: str
    input: str
    additional_input: Dict[str, Any]
    created_at: sa.DateTime
    modified_at: sa.DateTime
    artifacts: List["ArtifactModel"] = dataclasses.field(default_factory=list)

@dataclass
class StepModel:
    step_id: str
    task_id: str
    name: str
    input: str
    status: str
    output: str
    is_last: bool
    created_at: sa.DateTime
    modified_at: sa.DateTime
    additional_input: Dict[str, Any]
    additional_output: Dict[str, Any]
    artifacts: List["ArtifactModel"] = dataclasses.field(default_factory=list)

@dataclass
class ArtifactModel:
    artifact_id: str
    task_id: str
    step_id: str
    agent_created: bool
    file_name: str
    relative_path: str
    created_at: sa.DateTime
    modified_at: sa.DateTime
    step: Optional["StepModel"] = None
    task: Optional["TaskModel"] = None

class Database:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_async_engine(url)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def session(self):
        async with self.engine.connect() as connection:
            async with connection.begin() as transaction:
                session = self.Session()
                session.connection(connection)
                session.transaction(transaction)
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise
                else:
                    await session.commit()
                finally:
                    await session.close()

def convert_to_task(task_obj: TaskModel) -> Task:
    task_artifacts = [convert_to_artifact(artifact) for artifact in task_obj.artifacts]
    return Task(
        task_id=task_obj.task_id,
        created_at=task_obj.created_at,
        modified_at=task_obj.modified_at,
        input=task_obj.input,
        additional_input=task_obj.additional_input,
        artifacts=task_artifacts,
    )

def convert_to_step(step_model: StepModel) -> Step:
    step_artifacts = [
        convert_to_artifact(artifact) for artifact in step_model.artifacts
    ]
    status = Status.completed if step_model.status == "completed" else Status.created
    return Step(
        task_id=step_model.task_id,
        step_id=step_model.step_id,
        created_at=step_model.created_at,
        modified_at=step_model.modified_at,
        name=step_model.name,
        input=step_model.input,
        status=status,
        output=step_model.output,
        artifacts=step_artifacts,
        is_last=step_model.is_last,
        additional_input=step_model.additional_input,
        additional_output=step_model.additional_output,
    )

def convert_to_artifact(artifact_model: ArtifactModel) -> Artifact:
    return Artifact(
        artifact_id=artifact_model.artifact_id,
        created_at=artifact_model.created_at,
        modified_at=artifact_model.modified_at,
        agent_created=artifact_model.agent_created,
        relative_path=artifact_model.relative_path,
        file_name=artifact_model.file_name,
    )

class AgentDB:
    def __init__(self, db: Database):
        self.db = db

    async def create_task(
        self, input: Optional[str], additional_input: Optional[dict] = {}
    ) -> Task:
        async with self.db.session() as session:
            new_task = TaskModel(
                task_id=str(uuid.uuid4()),
                input=input,
                additional_input=additional_input if additional_input else {},
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return convert_to_task(new_task)

    async def create_step(
        self,
        task_id: str,
        input: StepRequestBody,
        is_last: bool = False,
        additional_input: Optional[Dict[str, Any]] = {},
    ) -> Step:
        async with self.db.session() as session:
            new_step = StepModel(
                task_id=task_id,
                step_id=
