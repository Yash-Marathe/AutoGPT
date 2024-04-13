import enum
from pathlib import Path
from typing import Optional

import boto3
from google.cloud import storage
from pydantic import BaseModel

from .base import FileWorkspace


class FileWorkspaceBackendName(str, enum.Enum):
    LOCAL = "local"
    GCS = "gcs"
    S3 = "s3"


class FileWorkspaceConfiguration(BaseModel):
    root: Path


class LocalFileWorkspaceConfiguration(FileWorkspaceConfiguration):
    def __init__(self, root: Path):
        super().__init__(root=root)


class S3FileWorkspaceConfiguration(FileWorkspaceConfiguration):
    def __init__(self, root: Path):
        self.root = root
        self.s3 = boto3.resource("s3")


class GCSFileWorkspaceConfiguration(FileWorkspaceConfiguration):
    def __init__(self, root: Path):
        self.root = root
        self.client = storage.Client()


class LocalFileWorkspace(FileWorkspace):
    def __init__(self, config: LocalFileWorkspaceConfiguration):
        self.config = config


class S3FileWorkspace(FileWorkspace):
    def __init__(self, config: S3FileWorkspaceConfiguration):
        self.config = config
        self.bucket = config.s3.Bucket(config.root.parent.name)


class GCSFileWorkspace(FileWorkspace):
    def __init__(self, config: GCSFileWorkspaceConfiguration):
        self.config = config
        self.bucket = self.config.client.get_bucket(config.root.parent.name)



