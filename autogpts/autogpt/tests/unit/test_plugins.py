import os
import pathlib
import typing as t
from unittest import TestCase, skip

import yaml

from autogpt.config.config import Config
from autogpt.plugins import inspect_zip_for_modules, scan_plugins
from autogpt.plugins.plugin_config import PluginConfig
from autogpt.plugins.plugins_config import PluginsConfig

PLUGINS_TEST_DIR = pathlib.Path("tests/unit/data/test_plugins")
PLUGIN_TEST_ZIP_FILE = "Auto-GPT-Plugin-Test-master.zip"
PLUGIN_TEST_INIT_PY = "Auto-GPT-Plugin-Test-master/src/auto_gpt_vicuna/__init__.py"
PLUGIN_TEST_OPENAI = "https://weathergpt.vercel.app/"

class TestPlugins(TestCase):

    def setUp(self) -> None:
        self.config = Config()

    @skip("Test is not yet implemented")
    def test_scan_plugins_openai(self, config: Config):
        pass

    def test_scan_plugins_generic(self, config: Config):
        config.plugins_config.plugins["auto_gpt_guanaco"] = PluginConfig(
            name="auto_gpt_guanaco", enabled=True
        )
        config.plugins_config.plugins["AutoGPTPVicuna"] = PluginConfig(
            name="AutoGPTPVicuna", enabled=True
        )
        result = scan_plugins(config)
        plugin_class_names = [plugin.__class__.__name__ for plugin in result]

        self.assertEqual(len(result), 2)
        self.assertIn("AutoGPTGuanaco", plugin_class_names)
        self.assertIn("AutoGPTPVicuna", plugin_class_names)

    def test_scan_plugins_not_enabled(self, config: Config):
        config.plugins_config.plugins["auto_gpt_guanaco"] = PluginConfig(
            name="auto_gpt_guanaco", enabled=True
        )
        config.plugins_config.plugins["auto_gpt_vicuna"] = PluginConfig(
            name="auto_gpt_vicuna", enabled=False
        )
        result = scan_plugins(config)
        plugin_class_names = [plugin.__class__.__name__ for plugin in result]

        self.assertEqual(len(result), 1)
        self.assertIn("AutoGPTGuanaco", plugin_class_names)
        self.assertNotIn("AutoGPTPVicuna", plugin_class_names)

    def test_inspect_zip_for_modules(self):
        result = inspect_zip_for_modules(str(PLUGINS_TEST_DIR / PLUGIN_TEST_ZIP_FILE))
        self.assertEqual(result, [PLUGIN_TEST_INIT_PY])

    def test_create_base_config(self, config: Config):
        config.plugins_allowlist = ["a", "b"]
        config.plugins_denylist = ["c", "d"]

        plugins_config = PluginsConfig.load_config(
            plugins_config_file=config.plugins_config_file,
            plugins_denylist=config.plugins_denylist,
            plugins_allowlist=config.plugins_allowlist,
        )

        self.assertEqual(len(plugins_config.plugins), 4)
        self.assertTrue(plugins_config.get("a").enabled)
        self.assertTrue(plugins_config.get("b").enabled)
        self.assertFalse(plugins_config.get("c").enabled)
        self.assertFalse(plugins_config.get("d").enabled)

        with open(config.plugins_config_file, "r") as saved_config_file:
            saved_config = yaml.load(saved_config_file, Loader=yaml.FullLoader)

        self.assertEqual(saved_config, {
            "a": {"enabled": True, "config": {}},
            "b": {"enabled": True, "config": {}},
            "c": {"enabled": False, "config": {}},
            "d": {"enabled": False, "config": {}},
        })

    def test_load_config(self, config: Config):
        test_config = {
            "a": {"enabled": True, "config": {"api_key": "1234"}},
            "b": {"enabled": False, "config": {}},
        }
        with open(config.plugins_config_file, "w+") as f:
            f.write(yaml.dump(test_config))

        plugins_config = PluginsConfig.load_config(
            plugins_config_file=config.plugins_config_file,
            plugins_denylist=config.plugins_denylist,
            plugins_allowlist=config.plugins_allowlist,
        )

        self.assertEqual(len(plugins_config.plugins), 2)
        self.assertTrue(plugins_config.get("a").enabled)
        self.assertEqual(plugins_config.get("a").config, {"api_key": "1234"})
        self.assertFalse(plugins_config.get("b").enabled)
        self.assertEqual(plugins_config.get("b").config, {})
