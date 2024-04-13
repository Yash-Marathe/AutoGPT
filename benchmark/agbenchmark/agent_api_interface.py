import asyncio
import json
import logging
import os
import pathlib
import time
from typing import Any, Dict, Optional

import aiohttp
from aiohttp import ClientSession
from agbenchmark.__main__ import TEMP_FOLDER_ABS_PATH, UPDATES_JSON_PATH
from agbenchmark.agent_interface import get_list_of_file_paths
from agbenchmark.agent_protocol_client import (
    AgentApi,
    ApiClient,
    Configuration,
    TaskRequestBody,
)
from agbenchmark.agent_protocol_client.models.step import Step
from agbenchmark.utils.data_types import ChallengeData

LOG = logging.getLogger(__name__)


async def run_api_agent(
    task: ChallengeData, config: Dict[str, Any], artifacts_location: str, timeout: int
) -> None:
    host_value = config["AgentBenchmarkConfig"].host + "/ap/v1"

    configuration = Configuration(host=host_value)
    async with ApiClient(configuration) as api_client, ClientSession() as session:
        api_instance = AgentApi(api_client)
        task_request_body = TaskRequestBody(input=task.task)

        start_time = time.time()
        response = await api_instance.create_agent_task(
            task_request_body=task_request_body, session=session
        )
        task_id = response.task_id

        await upload_artifacts(
            api_instance, artifacts_location, task_id, "artifacts_in", session
        )

        i = 1
        steps_remaining = True
        while steps_remaining:
            step = await api_instance.execute_agent_task_step(task_id=task_id, session=session)
            await append_updates_file(step)

            print(f"[{task.name}] - step {step.name} ({i}. request)")
            i += 1

            if time.time() - start_time > timeout:
                raise TimeoutError("Time limit exceeded")
            if not step or step.is_last:
                steps_remaining = False
        if os.getenv("IS_MOCK"):
            await upload_artifacts(
                api_instance, artifacts_location, task_id, "artifacts_out", session
            )

        await copy_agent_artifacts_into_temp_folder(api_instance, task_id, session)


async def copy_agent_artifacts_into_temp_folder(api_instance, task_id, session):
    artifacts = await api_instance.list_agent_task_artifacts(task_id=task_id, session=session)
    for artifact in artifacts.artifacts:
        directory_location = pathlib.Path(TEMP_FOLDER_ABS_PATH)
        if artifact.relative_path:
            path = (
                artifact.relative_path
                if not artifact.relative_path.startswith("/")
                else artifact.relative_path[1:]
            )
            directory_location = pathlib.Path(
                os.path.dirname(directory_location / path)
            )
            LOG.info(f"Creating directory {directory_location}")

        directory_location.mkdir(parents=True, exist_ok=True)

        file_path = directory_location / artifact.file_name
        LOG.info(f"Writing file {file_path}")
        async with session.get(artifact.download_url) as resp:
            content = await resp.read()

        with open(file_path, "wb") as f:
            f.write(content)


async def append_updates_file(step: Step):
    with open(UPDATES_JSON_PATH, "r") as file:
        existing_data = json.load(file)
    # Append the new update to the existing array
    new_update = create_update_json(step)

    existing_data.append(new_update)
    # Write the updated array back to the file
    with open(UPDATES_JSON_PATH, "w") as file:
        file.write(json.dumps(existing_data, indent=2))


async def upload_artifacts(
    api_instance: AgentApi,
    artifacts_location: str,
    task_id: str,
    type: str,
    session: ClientSession,
) -> None:
    for file_path in get_list_of_file_paths(artifacts_location, type):
        relative_path: Optional[str] = "/".join(
            file_path.split(f"{type}/", 1)[-1].split("/")[:-1]
        )
        if not relative_path:
            relative_path = None

        async with session.post(
            api_instance.upload_agent_task_artifacts_url,
            data={"task_id": task_id, "file": open(file_path, "rb")},
            headers={"Content-Type": "multipart/form-data"},
        ) as resp:
            print(await resp.text())


def create_update_json(step: Step):
    now = int(time.time())
    content = {"content": step.to_dict(), "timestamp": now}

    return content
