import json
import os
from pathlib import Path
from typing import Any, Dict, Union

from .config import LOG_DIR

DEFAULT_PREFIX = "agent"
CURRENT_CONTEXT_FILE_NAME = "current_context.json"
NEXT_ACTION_FILE_NAME = "next_action.json"
PROMPT_SUMMARY_FILE_NAME = "prompt_summary.json"
SUMMARY_FILE_NAME = "summary.txt"
SUPERVISOR_FEEDBACK_FILE_NAME = "supervisor_feedback.txt"
PROMPT_SUPERVISOR_FEEDBACK_FILE_NAME = "prompt_supervisor_feedback.json"
USER_INPUT_FILE_NAME = "user_input.txt"

class LogCycleHandler:
    """
    A class for logging cycle data.
    """

    def __init__(self):
        self.log_count_within_cycle = 0

    def create_directory_path(self, directory_name: str, base_directory: Path, postfix: str) -> Path:
        directory_path = base_directory / directory_name / postfix
        if not directory_path.exists():
            directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path

    def get_agent_short_name(self, ai_name: str) -> str:
        return ai_name[:15].rstrip() if ai_name else DEFAULT_PREFIX

    def log_cycle(
        self,
        ai_name: str,
        created_at: str,
        cycle_count: int,
        data: Union[Dict[str, Any], Any],
        file_name: str,
    ) -> None:
        """
        Log cycle data to a JSON file.

        Args:
            data (Any): The data to be logged.
            file_name (str): The name of the file to save the logged data.
        """
        outer_folder_name = f"{created_at}_{self.get_agent_short_name(ai_name)}"
        outer_folder_path = self.create_directory_path(outer_folder_name, LOG_DIR, "DEBUG")

        nested_folder_name = str(cycle_count).zfill(3)
        nested_folder_path = self.create_directory_path(nested_folder_name, outer_folder_path, "")

        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        log_file_path = nested_folder_path / f"{self.log_count_within_cycle}_{file_name}"

        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(json_data + "\n")

        self.log_count_within_cycle += 1
