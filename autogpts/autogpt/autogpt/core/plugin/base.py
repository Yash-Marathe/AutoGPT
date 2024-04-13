import abc
from enum import Enum
from typing import Type, TypeVar

import pydantic
from pydantic import BaseModel

from autogpt.core.configuration import SystemConfiguration, UserConfigurable

PluginType = TypeVar("PluginType", bound="AbstractPlugin")

class PluginStorageFormat(str, Enum):
    INSTALLED_PACKAGE = "installed_package"
    WORKSPACE = "workspace"
    GIT = "git"
    PYPI = "pypi"

class PluginStorageRoute(str):
    pass

class PluginLocation(SystemConfiguration):
    storage_format: PluginStorageFormat = UserConfigurable()
    storage_route: PluginStorageRoute = UserConfigurable()

class AbstractPlugin(metaclass=abc.ABCMeta):
    pass

class PluginMetadata(BaseModel):
    name: str
    description: str
    location: PluginLocation

class PluginService(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_plugin(plugin_location: PluginLocation) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_file_path(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_import_path(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def resolve_name_to_path(
        plugin_route: PluginStorageRoute, path_type: str
    ) -> PluginStorageRoute:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_workspace(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_installed_package(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_git(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @staticmethod
    @abc.abstractmethod
    def load_from_pypi(plugin_route: PluginStorageRoute) -> PluginType:
        pass

    @classmethod
    def load_plugin(cls, plugin_location: PluginLocation) -> PluginType:
        if plugin_location.storage_format == PluginStorageFormat.INSTALLED_PACKAGE:
            return cls.load_from_installed_package(plugin_location.storage_route)
        elif plugin_location.storage_format == PluginStorageFormat.WORKSPACE:
            return cls.load_from_workspace(plugin_location.storage_route)
        elif plugin_location.storage_format == PluginStorageFormat.GIT:
            return cls.load_from_git(plugin_location.storage_route)
        elif plugin_location.storage_format == PluginStorageFormat.PYPI:
            return cls.load_from_pypi(plugin_location.storage_route)
        else:
            raise ValueError(f"Unsupported storage format: {plugin_location.storage_format}")

    __init_subclass__ = abc.abstractmethod(abc.ABC.__init_subclass__)
