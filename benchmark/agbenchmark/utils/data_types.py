import datetime
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr, validator


class DifficultyLevel(Enum):
    interface = "interface"
    basic = "basic"
    novice = "novice"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"
    human = "human"


DIFFICULTY_MAP = {
    DifficultyLevel.interface: 1,
    DifficultyLevel.basic: 2,
    DifficultyLevel.novice: 3,
    DifficultyLevel.intermediate: 4,
    DifficultyLevel.advanced: 5,
    DifficultyLevel.expert: 6,
    DifficultyLevel.human: 7,
}

STRING_DIFFICULTY_MAP = {e.value: DIFFICULTY_MAP[e] for e in DifficultyLevel}


def calculate_info_test_path(base_path: Path, benchmark_start_time: datetime) -> Path:
    base_path.mkdir(parents=True, exist_ok=True)
    date_stamp = benchmark_start_time.strftime("%Y%m%dT%H%M%S")
    run_name = "full_run"
    arg_labels = {
        "--test": None,
        "--category": None,
        "--maintain": "maintain",
        "--improve": "improve",
        "--explore": "explore",
    }
    for arg, label in arg_labels.items():
        if arg in sys.argv:
            test_arg = sys.argv[sys.argv.index(arg) + 1] if label is None else None
            run_name = arg.strip("--")
            if test_arg:
                run_name = f"{run_name}_{test_arg}"
            break
    report_path = base_path / f"{date_stamp}_{run_name}"
    report_path.mkdir(exist_ok=True)
    return report_path


class AgentBenchmarkConfig(BaseModel):
    agent_benchmark_config_path: Path | None = None
    reports_folder: Path | None = None
    host: str | None

    def __post_init__(self):
        if self.reports_folder is None:
            self.reports_folder = Path.cwd() / "agbenchmark_config" / "reports"

    def get_reports_location(self) -> Path:
        return self.reports_folder

    def get_reports_path(self, benchmark_start_time: datetime) -> Path:
        return calculate_info_test_path(self.get_reports_location(), benchmark_start_time)

    def get_regression_reports_path(self) -> Path:
        return self.get_reports_location() / "regression_tests.json"

    def get_success_rate_path(self) -> Path:
        return self.get_reports_location() / "success_rate.json"

    def get_agent_home_directory(self) -> Path:
        return Path(self.agent_benchmark_config_path).resolve().parent

    def to_dict(self) -> dict:
        return self.dict()

    def to_json(self, path: Path | str) -> None:
        path = Path(path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as file:
            json.dump(self.to_dict(), file, indent=4)


class Info(BaseModel):
    difficulty: DifficultyLevel
    description: constr(regex=r"^Tests if the agent can.*")
    side_effects: List[str]

    @validator("difficulty", pre=True)
    def difficulty_to_enum(cls: "Info", v: str | DifficultyLevel) -> DifficultyLevel:
        if isinstance(v, DifficultyLevel):
            return v
        if isinstance(v, str):
            try:
                return DifficultyLevel(v.lower())
            except ValueError:
                pass
        raise ValueError(f"Cannot convert {v} to DifficultyLevel.")


class Eval(BaseModel):
    type: str
    scoring: Optional[str]
    template: Optional[str]
    examples: Optional[str]

    @validator("scoring", "template", always=True)
    def validate_eval_fields(cls, v, values, field):
        if "type" in values and values["type"] == "llm":
            if v is None:
                raise ValueError(f"{field.name} must be provided when type is 'llm'")
        else:
            if v is not None:
                raise ValueError(f"{field.name} should only exist when type is 'llm'")
        return v

    @validator("scoring")
    def validate_scoring(cls, v):
