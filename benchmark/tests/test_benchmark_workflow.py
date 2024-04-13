import pytest
import requests
from datetime import datetime, timezone
import time

URL_BENCHMARK = "http://localhost:8080/ap/v1"
URL_AGENT = "http://localhost:8000/ap/v1"

@pytest.fixture
def base_url():
    return URL_BENCHMARK

@pytest.fixture
def task_id(base_url):
    task_request = {"eval_id": "021c695a-6cc4-46c2-b93a-f3a9b0f4d123", "input": "Write the word 'Washington' to a .txt file"}
    response = requests.post(f"{base_url}/agent/tasks", json=task_request)
    return response.json()["task_id"]

@pytest.fixture
def retry(request):
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        if outcome.get("failed"):
            pytest.terminal_reporter.isatty and pytest.raises(Exception, lambda: call.funcargs[request.param]())
        else:
            call.funcargs[request.param].__wrapped__()

@pytest.fixture
def timestamp():
    return datetime.now(timezone.utc)

