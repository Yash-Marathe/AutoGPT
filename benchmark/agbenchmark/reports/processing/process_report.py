import json
import os
from pathlib import Path
from typing import Any, Dict

from agbenchmark.reports.processing.get_files import (
    get_latest_report_from_agent_directories,
)
from agbenchmark.reports.processing.report_types import Report, Test
from agbenchmark.utils.data_types import STRING_DIFFICULTY_MAP


def get_reports_data(report_path: str) -> Dict[str, Report]:
    latest_files = get_latest_report_from_agent_directories(report_path)

    if not latest_files:
        raise Exception("No files found in the reports directory")

    reports_data = {}
    for subdir, file in latest_files:
        subdir_name = os.path.basename(os.path.normpath(subdir))
        report_file = Path(subdir) / file
        with open(report_file, "r") as f:
            json_data = json.load(f)
            report_data = Report.parse_obj(json_data)
            reports_data[subdir_name] = report_data

    return reports_data


def get_agent_category(report: Report) -> Dict[str, int]:
    categories: Dict[str, int] = {}

    def get_highest_category_difficulty(data: Test) -> None:
        for category in data.category:
            if category in {"interface", "iterate", "product_advisor"}:
                continue
            categories.setdefault(category, 0)
            if data.metrics.success:
                num_dif = STRING_DIFFICULTY_MAP[data.metrics.difficulty]
                if num_dif > categories[category]:
                    categories[category] = num_dif

    for _, test_data in report.tests.items():
        get_highest_category_difficulty(test_data)

    return categories


def all_agent_categories(reports_data: Dict[str, Report]) -> Dict[str, Dict[str, int]]:
    all_categories: Dict[str, Dict[str, int]] = {}

    for name, report in reports_data.items():
        categories = get_agent_category(report)
        if categories:  # only add to all_categories if categories is not empty
            all_categories[name] = categories

    return all_categories
