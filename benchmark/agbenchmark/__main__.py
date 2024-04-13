import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import pytest

import helicone.lock  # type: ignore
import toml
from helicone.lock import HeliconeLockManager
from helicone.lock.exceptions import HeliconeLockError  # type: ignore

from agbenchmark.app import app
from agbenchmark.reports.ReportManager import SingletonReportManager
from agbenchmark.utils.data_types import AgentBenchmarkConfig

CURRENT_DIRECTORY = Path(__file__).resolve().parent
CONFIG_DIR = CURRENT_DIRECTORY / "agbenchmark_config"
CONFIG_FILE = CONFIG_DIR / "config.json"
TEMP_FOLDER_PATH = CONFIG_DIR / "temp_folder"
CHALLENGES_ALREADY_BEATEN_PATH = CONFIG_DIR / "challenges_already_beaten.json"
UPDATES_JSON_PATH = CONFIG_DIR / "updates.json"
BENCHMARK_START_TIME_DT = datetime.now(timezone.utc)
BENCHMARK_START_TIME = BENCHMARK_START_TIME_DT.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def get_unique_categories() -> Set[str]:
    categories: Set[str] = set()
    challenges_dir = CURRENT_DIRECTORY / "challenges"

    for data_file in glob.glob(str(challenges_dir / "**" / "data.json"), recursive=True):
        try:
            with open(data_file, "r") as f:
                data = json.load(f)
                categories.update(data.get("category", []))
        except json.JSONDecodeError:
            print(f"Error: {data_file} is not a valid JSON file.")
        except IOError:
            print(f"IOError: file could not be read: {data_file}")

    return categories


def run_benchmark(
    maintain: bool = False,
    improve: bool = False,
    explore: bool = False,
    mock: bool = False,
    no_dep: bool = False,
    nc: bool = False,
    keep_answers: bool = False,
    category: Optional[List[str]] = None,
    skip_category: Optional[List[str]] = None,
    test: Optional[str] = None,
    cutoff: Optional[int] = None,
    server: bool = False,
) -> int:
    # Check if configuration file exists and is not empty
    if not CONFIG_FILE.exists() or not CONFIG_FILE.stat().st_size > 0:
        print("Error: benchmark_config.json is missing or empty.")
        return 1

    initialize_updates_file()
    SingletonReportManager()

    try:
        with open(CONFIG_FILE, "r") as f:
            agent_benchmark_config = AgentBenchmarkConfig(**json.load(f))
            agent_benchmark_config.agent_benchmark_config_path = str(CONFIG_FILE)
    except json.JSONDecodeError:
        print("Error: benchmark_config.json is not a valid JSON file.")
        return 1

    if maintain and improve and explore:
        print(
            "Error: You can't use --maintain, --improve or --explore at the same time. Please choose one."
        )
        return 1

    if test and (category or skip_category or maintain or improve or explore):
        print(
            "Error: If you're running a specific test make sure no other options are selected. Please just pass the --test."
        )
        return 1

    print("Current configuration:")
    for key, value in vars(agent_benchmark_config).items():
        print(f"{key}: {value}")

    pytest_args = ["-vs"]
    if keep_answers:
        pytest_args.append("--keep-answers")

    if test:
        print("Running specific test:", test)
    else:
        categories = get_unique_categories()

        if category:
            invalid_categories = set(category) - categories
            if invalid_categories:
                print(
                    f"Invalid categories: {invalid_categories}. Valid categories are: {categories}"
                )
                return 1

        if category:
            categories_to_run = set(category)
            if skip_category:
                categories_to_run -= set(skip_category)
                if not categories_to_run:
                    print("Error: You can't skip all categories")
                    return 1
            pytest_args.extend(["-m", " or ".join(categories_to_run), "--category"])
            print("Running tests of category:", categories_to_run)
        elif skip_category:
            categories_to_run = categories - set(skip_category)
            if not categories_to_run:
                print("Error: You can't skip all categories")
                return 1
            pytest_args.extend(["-m", " or ".join(categories_to_run), "--category"])
            print("Running tests of category:", categories_to_run)
        else:
            print("Running all categories")

        if maintain:
            print("Running only regression tests")
            pytest_args.append("--maintain")
        elif improve:
            print
