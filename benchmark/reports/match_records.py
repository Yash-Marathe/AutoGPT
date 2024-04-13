import glob
import json
import os

import pandas as pd
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union

class Metrics(BaseModel):
    difficulty: str
    success: bool
    success_percent: float = Field(..., alias="success_%")
    run_time: Optional[str] = None
    fail_reason: Optional[str] = None
    attempted: Optional[bool] = None


class MetricsOverall(BaseModel):
    run_time: str
    highest_difficulty: str
    percentage: Optional[float] = None


class Test(BaseModel):
    data_path: str
    is_regression: bool
    answer: str
    description: str
    metrics: Metrics
    category: List[str]
    task: Optional[str] = None
    reached_cutoff: Optional[bool] = None


class SuiteTest(BaseModel):
    data_path: str
    metrics: MetricsOverall
    tests: Dict[str, Test]
    category: Optional[List[str]] = None
    task: Optional[str] = None
    reached_cutoff: Optional[bool] = None


class Report(BaseModel):
    command: str
    completion_time: str
    benchmark_start_time: str
    metrics: MetricsOverall
    tests: Dict[str, Union[Test, SuiteTest]]
    config: Dict[str, str | dict[str, str]]


def get_reports() -> pd.DataFrame:
    """Get report data from the reports directory."""
    report_data = []
    current_dir = os.getcwd()
    reports_dir = current_dir if current_dir.endswith("reports") else "reports"

    for agent_name in os.listdir(reports_dir):
        agent_dir = os.path.join(reports_dir, agent_name)
        if not os.path.isdir(agent_dir):
            continue

        report_files = [
            os.path.join(run_dir, "report.json")
            for run_dir in glob.glob(os.path.join(agent_dir, "*"))
            if os.path.isdir(run_dir)
        ]

        for report_file in report_files:
            if not os.path.isfile(report_file):
                continue

            with open(report_file, "r") as f:
                json_data = json.load(f)
                report = Report.parse_obj(json_data)

                for test_name, test_data in report.tests.items():
                    test_json = {
                        "agent": agent_name.lower(),
                        "benchmark_start_time": report.benchmark_start_time,
                    }

                    if isinstance(test_data, SuiteTest):
                        if test_data.category:  # this means it's a same task test
                            # ...
                        else:  # separate tasks in 1 suite
                            # ...
                    else:
                        # ...

                    report_data.append(test_json)

    return pd.DataFrame(report_data)


def get_helicone_data() -> pd.DataFrame:
    # ...


if __name__ == "__main__":
    # ...

    reports_df = get_reports()
    reports_df.to_pickle("raw_reports.pkl")
    helicone_df = get_helicone_data()
    helicone_df.to_pickle("raw_helicone.pkl")

    # ...

    helicone_df["benchmark_start_time"] = pd.to_datetime(
        helicone_df["benchmark_start_time"].apply(try_formats), utc=True, errors="coerce"
    )
    helicone_df = helicone_df.dropna(subset=["benchmark_start_time"])

    # ...

    assert pd.api.types.is_datetime64_any_dtype(
        helicone_df["benchmark_start_time"]
    ), "benchmark_start_time in helicone_df is not datetime"

    # ...
