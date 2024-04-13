import copy
import logging
import os
import pathlib
from io import BytesIO
from typing import Any
from uuid import uuid4

import orjson
from fastapi import APIRouter, FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from forge.sdk.db import AgentDB
from forge.sdk.errors import NotFoundError
from forge.sdk.model import (
    Artifact,
    Step,
    StepRequestBody,
    Task,
    TaskArtifactsListResponse,
    TaskListResponse,
    TaskStepsListResponse,
)
from forge.sdk.routes.agent_protocol import base_router
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig

from autogpt.agent_factory.configurators import configure_agent_with_state
from autogpt.agent_factory.generators import generate_agent_for_task
from autogpt.agent_manager import AgentManager
from autogpt.commands.system import finish
from autogpt.commands.user_interaction import ask_user
from autogpt.config import Config
from autogpt.core.resource.model_providers import ChatModelProvider
from autogpt.file_workspace import (
    FileWorkspace,
    FileWorkspaceBackendName,
    get_workspace,
)
from autogpt.logs.utils import fmt_kwargs
from autogpt.models.action_history import ActionErrorResult, ActionSuccessResult

logger = logging.getLogger(__name__)

class AgentProtocolServer:
    # ... (rest of the class remains the same)

def task_agent_id(task_id: str | int) -> str:
    return f"AutoGPT-{task_id}"
