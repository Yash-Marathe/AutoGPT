from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from pydantic import BaseModel

class PluginConfig(BaseModel):
    """Class for holding plugin configuration"""

    name: str
    enabled: bool
    config: Dict[str, Any]

class PluginsConfig(BaseModel):
    """Class for holding configuration of all plugins"""

    plugins: Dict[str, PluginConfig]

    def __repr__(self) -> str:
        return f"PluginsConfig({self.plugins})"

    def get(self, name: str) -> Union[PluginConfig, None]:
        return self.plugins.get(name)

    def is_enabled(self, name: str) -> bool:
        plugin_config = self.plugins.get(name)
        return plugin_config is not None and plugin_config.enabled

    @classmethod
    def load_config(
        cls,
        plugins_config_file: Path,
        plugins_denylist: list[str],
        plugins_allowlist: list[str],
    ) -> PluginsConfig:
        empty_config = cls(plugins={})

        try:
            config_data = cls.deserialize_config_file(
                plugins_config_file,
                plugins_denylist,
                plugins_allowlist,
            )
            if not isinstance(config_data, dict):
                logger.error(
                    f"Expected plugins config to be a dict, got {type(config_data)}."
                    " Continuing without plugins."
                )
                return empty_config
            return cls(plugins=config_data)

        except BaseException as e:
            logger.error(
                f"Plugin config is invalid. Continuing without plugins. Error: {e}"
            )
            return empty_config

    @classmethod
    def deserialize_config_file(
        cls,
        plugins_config_file: Path,
        plugins_denylist: list[str],
        plugins_allowlist: list[str],
    ) -> Dict[str, PluginConfig]:
        if not plugins_config_file.exists():
            logger.warning("plugins_config.yaml does not exist, creating base config.")
            cls.create_empty_plugins_config(
                plugins_config_file,
                plugins_denylist,
                plugins_allowlist,
            )

        with open(plugins_config_file, "r") as f:
            plugins_config = yaml.safe_load(f)

        plugins = {}
        for name, plugin in plugins_config.items():
            if isinstance(plugin, dict):
                plugins[name] = PluginConfig(
                    name=name,
                    enabled=plugin.get("enabled", False),
                    config=plugin.get("config", {}),
                )
            elif isinstance(plugin, PluginConfig):
                plugins[name] = plugin
            else:
                raise ValueError(f"Invalid plugin config data type: {type(plugin)}")
        return plugins

    @staticmethod
    def create_empty_plugins_config(
        plugins_config_file: Path,
        plugins_denylist: list[str],
        plugins_allowlist: list[str],
    ):
        """
        Create an empty plugins_config.yaml file.
        Fill it with values from old env variables.
        """
        base_config = {}

        logger.debug(f"Legacy plugin denylist: {plugins_denylist}")
        logger.debug(f"Legacy plugin allowlist: {plugins_allowlist}")

        # Backwards-compatibility shim
        for plugin_name in plugins_denylist:
            base_config[plugin_name] = {"enabled": False, "config": {}}

        for plugin_name in plugins_allowlist:
            base_config[plugin_name] = {"enabled": True, "config": {}}

        logger.debug(f"Constructed base plugins config: {base_config}")

        logger.debug(f"Creating plugin config file {plugins_config_file}")
        plugins_config_file.write_text(yaml.dump(base_config))
        return base_config
