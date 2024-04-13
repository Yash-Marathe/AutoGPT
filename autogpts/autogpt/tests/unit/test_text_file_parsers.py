import json
import logging
import os
import pathlib
from typing import Any, Callable, Dict, List, NamedTemporaryFile, Optional

import docx
import pytest
import yaml
from bs4 import BeautifulSoup

import autogpt.commands.file_operations_utils as file_operations_utils

logger = logging.getLogger(__name__)

plain_text_str = "Hello, world!"


def create_mock_file(file_extension: str, file_content: str) -> pathlib.Path:
    temp_file = NamedTemporaryFile(mode="w", delete=False, suffix=f".{file_extension}")
    temp_file.write(file_content)
    temp_file.close()

    file_path = pathlib.Path(temp_file.name)
    return file_path


def create_mock_binary_file(file_extension: str) -> pathlib.Path:
    if file_extension == ".pdf":
        file_content = generate_pdf_content(plain_text_str)
    elif file_extension == ".docx":
        file_content = generate_docx_content(plain_text_str)
    else:
        raise ValueError(f"Unsupported binary file extension: {file_extension}")

    temp_file = NamedTemporaryFile(mode="wb", delete=False, suffix=f".{file_extension}")
    temp_file.write(file_content)
    temp_file.close()

    file_path = pathlib.Path(temp_file.name)
    return file_path


def generate_pdf_content(text: str) -> bytes:
    # Generate a minimal PDF file with the given text
    pass  # Implementation not provided here


def generate_docx_content(text: str) -> bytes:
    # Generate a minimal DOCX file with the given text
    pass  # Implementation not provided here


def decode_textual_file(file: pathlib.Path, file_extension: str, logger: logging.Logger) -> str:
    with open(file, "rb") as f:
        return file_operations_utils.decode_textual_file(f, file_extension, logger)


def is_file_binary(file: pathlib.Path) -> bool:
    with open(file, "rb") as f:
        return file_operations_utils.is_file_binary_fn(f)


def test_parsers() -> None:
    file_creation_functions: Dict[str, Callable[[str], pathlib.Path]] = {
        ".txt": create_mock_file,
        ".csv": create_mock_file,
        ".pdf": create_mock_binary_file,
        ".docx": create_mock_binary_file,
        ".json": create_mock_file,
        ".xml": create_mock_file,
        ".yaml": create_mock_file,
        ".html": create_mock_file,
        ".md": create_mock_file,
        ".tex": create_mock_file,
    }

    binary_files_extensions: List[str] = [".pdf", ".docx"]

    for file_extension, file_creator in file_creation_functions.items():
        created_file_path = file_creator(file_extension)

        loaded_text = decode_textual_file(created_file_path, file_extension, logger)
        assert plain_text_str in loaded_text

        should_be_binary = file_extension in binary_files_extensions
        assert should_be_binary == is_file_binary(created_file_path)

        created_file_path.unlink()  # Clean up
