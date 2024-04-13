import enum
from typing import Optional

from pydantic import BaseModel, Field

from autogpt.core.ability.schema import AbilityResult
from .task_context import TaskContext  # Import TaskContext after it is defined

class TaskType(str, enum.Enum):
    RESEARCH = "research"
    WRITE = "write"
    EDIT = "edit"
    CODE = "code"
    DESIGN = "design"
    TEST = "test"
    PLAN = "plan"

class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskContext(BaseModel):
    cycle_count: int = 0
    status: TaskStatus = TaskStatus.BACKLOG
    parent: Optional["Task"] = None
    prior_actions: list[AbilityResult] = Field(default_factory=list)
    memories: list = Field(default_factory=list)
    user_input: list[str] = Field(default_factory=list)
    supplementary_info: list[str] = Field(default_factory=list)
    enough_info: bool = False

class Task(BaseModel):
    objective: str
    type: TaskType  # Use TaskType enum instead of str
    priority: int
    ready_criteria: list[str]
    acceptance_criteria: list[str]
    context: TaskContext = Field(default_factory=TaskContext)

TaskContext.update_forward_refs()
