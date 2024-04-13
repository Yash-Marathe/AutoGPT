import base64
import json
import os
import re
from datetime import datetime, timedelta

import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Get the base64 string from the environment variable
base64_creds = os.getenv("GDRIVE_BASE64")

if base64_creds is None:
    raise ValueError("The GDRIVE_BASE64 environment variable is not set")

# Decode the base64 string into bytes
creds_bytes = base64.b64decode(base64_creds)

# Convert the bytes into a string
creds_string = creds_bytes.decode("utf-8")

# Parse the string into a JSON object
creds_info = json.loads(creds_string)

# Define the base directory containing JSON files
base_dir = "reports"

# Create a list to store each row of data
rows = []

def process_test(test_name, test_info, agent_name, common_data):
    """Recursive function to process test data."""
    parts = test_name.split("_", 1)  # Split by underscore only once
    test_suite = parts[0] if len(parts) > 1 else None

    # transform array into string with | as separator
    separator = "|"
    categories = separator.join(test_info.get("category", []))

    row = {
        "Agent": agent_name,
        "Command": common_data.get("command", ""),
        "Completion Time": common_data.get("completion_time", ""),
        "Benchmark Start Time": common_data.get("benchmark_start_time", ""),
        "Total Run Time": common_data.get("metrics", {}).get("run_time", ""),
        "Highest Difficulty": common_data.get("metrics", {}).get("highest_difficulty", ""),
        "Workspace": common_data.get("config", {}).get("workspace", ""),
        "Test Name": test_name,
        "Data Path": test_info.get("data_path", ""),
        "Is Regression": test_info.get("is_regression", ""),
        "Difficulty": test_info.get("metrics", {}).get("difficulty", ""),
        "Success": test_info.get("metrics", {}).get("success", ""),
        "Success %": test_info.get("metrics", {}).get("success_%", ""),
        "Non mock success %": test_info.get("metrics", {}).get("non_mock_success_%", ""),
        "Run Time": test_info.get("metrics", {}).get("run_time", ""),
        "Benchmark Git Commit Sha": common_data.get("benchmark_git_commit_sha", None),
        "Agent Git Commit Sha": common_data.get("agent_git_commit_sha", None),
        "Cost": test_info.get("metrics", {}).get("cost", ""),
        "Attempted": test_info.get("metrics", {}).get("attempted", ""),
        "Test Suite": test_suite,
        "Category": categories,
        "Task": test_info.get("task", ""),
        "Answer": test_info.get("answer", ""),
        "Description": test_info.get("description", ""),
        "Fail Reason": test_info.get("metrics", {}).get("fail_reason", ""),
        "Reached Cutoff": test_info.get("reached_cutoff", ""),
    }

    rows.append(row)

    # Check for nested tests and process them if present
    nested_tests = test_info.get("tests")
    if nested_tests:
        for nested_test_name, nested_test_info in nested_tests.items():
            process_test(nested_test_name, nested_test_info, agent_name, common_data)

# Loop over each directory in the base directory
for agent_dir in os.listdir(base_dir):
    agent_dir_path = os.path.join(base_dir, agent_dir)

    # Ensure the agent_dir_path is a directory
    if os.path.isdir(agent_dir_path):
        # Loop over each sub-directory in the agent directory (e.g., "folder49_07-28-03-53")
        for report_folder in os.listdir(agent_dir_path):
            report_folder_path = os.path.join(agent_dir_path, report_folder)

            # Ensure the report_folder_path is a directory
            if os.path.isdir(report_folder_path):
                # Check for a file named "report.json" in the sub-directory
                report_path = os.path.join(report_folder_path, "report.json")

                if os.path.exists(report_path):
                    # Load the JSON data from the file
                    with open(report_path, "r") as f:
                        data = json.load(f)

                    # Check if benchmark_start_time complies with the required format
                    benchmark_start_time = data.get("benchmark_start_time", "")
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00", benchmark_start_time):
                        continue

                    # Parse the benchmark_start_time to a datetime object
                    benchmark_datetime = datetime.strptime(benchmark_start_time, "%Y-%m-%dT%H:%M:%S+00:00")

                    # Check if benchmark_start_time is older than 3 days
                    current_datetime = datetime.utcnow()
                    if current_datetime - benchmark_
