import os
import shutil
import pytest

import pyworkspace  # Assuming the classes are defined in a file named workspace.py

# Constants
TEST_BASE_PATH = "/tmp/test_workspace"
TEST_FILE_CONTENT = b"Hello World"
TEST_TASK_ID = "1234"


@pytest.fixture
def setup_local_workspace():
    os.makedirs(TEST_BASE_PATH, exist_ok=True)
    yield TEST_BASE_PATH
    shutil.rmtree(TEST_BASE_PATH)  # Cleanup after tests


def test_local_read_write_delete_exists(setup_local_workspace):
    workspace = pyworkspace.LocalWorkspace(setup_local_workspace)

    # Write
    workspace.write(TEST_TASK_ID, "test_file.txt", TEST_FILE_CONTENT)

    # Exists
    assert workspace.exists(TEST_TASK_ID, "test_file.txt")

    # Read
    assert workspace.read(TEST_TASK_ID, "test_file.txt") == TEST_FILE_CONTENT

    # Delete
    workspace.delete(TEST_TASK_ID, "test_file.txt")
    assert not workspace.exists(TEST_TASK_ID, "test_file.txt")


def test_local_list(setup_local_workspace):
    workspace = pyworkspace.LocalWorkspace(setup_local_workspace)
    workspace.write(TEST_TASK_ID, "test1.txt", TEST_FILE_CONTENT)
    workspace.write(TEST_TASK_ID, "test2.txt", TEST_FILE_CONTENT)

    files = workspace.list(TEST_TASK_ID, ".")
    assert set(files) == {"test1.txt", "test2.txt"}
