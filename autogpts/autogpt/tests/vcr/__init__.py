import logging
import os
from hashlib import sha256
from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture
from vcr_cassettes import before_record_request, before_record_response, freeze_request_body

PROXY = os.environ.get("PROXY")
DEFAULT_RECORD_MODE = "new_episodes"


def get_vcr_config(record_mode=None):
    return {
        "before_record_request": before_record_request,
        "before_record_response": before_record_response,
        "filter_headers": [
            "Authorization",
            "AGENT-MODE",
            "AGENT-TYPE",
            "Cookie",
            "OpenAI-Organization",
            "X-OpenAI-Client-User-Agent",
            "User-Agent",
        ],
        "match_on": ["method", "headers"],
        "record_mode": record_mode or DEFAULT_RECORD_MODE,
    }


@pytest.fixture(scope="session")
def vcr_config(request):
    record_mode = request.config.getoption("--record-mode", default="new_episodes")
    return get_vcr_config(record_mode)


@pytest.fixture(scope="function")
def vcr_cassette_dir(request):
    test_name = os.path.splitext(request.node.name)[0]
    cassette_dir = os.path.join("tests/vcr_cassettes", test_name)
    os.makedirs(cassette_dir, exist_ok=True)
    yield cassette_dir
    os.rmdir(cassette_dir)


def patch_api_base(requestor: openai.api_requestor.APIRequestor):
    new_api_base = f"{PROXY}/v1"
    requestor.api_base = new_api_base
    return requestor


@pytest.fixture
def patched_api_requestor(mocker: MockerFixture):
    init_requestor = openai.api_requestor.APIRequestor.__init__
    prepare_request = openai.api_requestor.APIRequestor._prepare_request_raw

    def patched_init_requestor(requestor, *args, **kwargs):
        init_requestor(requestor, *args, **kwargs)
        patch_api_base(requestor)

    def patched_prepare_request(self, *args, **kwargs):
        url, headers, data = prepare_request(self, *args, **kwargs)

        if PROXY:
            headers["AGENT-MODE"] = os.environ.get("AGENT_MODE")
            headers["AGENT-TYPE"] = os.environ.get("AGENT_TYPE")

        logging.getLogger("patched_api_requestor").debug(
            f"Outgoing API request: {headers}\n{data.decode() if data else None}"
        )

        # Add hash header for cheap & fast matching on cassette playback
        headers["X-Content-Hash"] = sha256(
            freeze_request_body(data), usedforsecurity=False
        ).hexdigest()

        return url, headers, data

    if PROXY:
        mocker.patch.object(
            openai.api_requestor.APIRequestor,
            "__init__",
            new=patched_init_requestor,
        )
    mocker.patch.object(
        openai.api_requestor.APIRequestor,
        "_prepare_request_raw",
        new=patched_prepare_request,
    )
    yield
    mocker.resetall()
