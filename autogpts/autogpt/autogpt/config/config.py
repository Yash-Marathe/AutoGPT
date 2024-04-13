from typing import Literal, Optional, Union
from pathlib import Path
from pydantic import BaseSettings, Field, validator, conint, conlist
from autogpt.core.resource.model_providers.openai import OPEN_AI_CHAT_MODELS
from autogpt.file_workspace import FileWorkspaceBackendName
from autogpt.logs.config import LoggingConfig
from autogpt.plugins.plugins_config import PluginsConfig
from autogpt.speech import TTSConfig

PROJECT_ROOT = Path(__file__).parent.parent
AI_SETTINGS_FILE = Path("ai_settings.yaml")
AZURE_CONFIG_FILE = Path("azure.yaml")
PLUGINS_CONFIG_FILE = Path("plugins_config.yaml")
PROMPT_SETTINGS_FILE = Path("prompt_settings.yaml")

GPT_4_MODEL = "gpt-4"
GPT_3_MODEL = "gpt-3.5-turbo"

class Config(BaseSettings):
    name: str = Field("Auto-GPT configuration", const=True)
    description: str = Field("Default configuration for the Auto-GPT application.", const=True)

    project_root: Path = Field(PROJECT_ROOT, const=True)
    app_data_dir: Path = Field(PROJECT_ROOT / "data", const=True)
    skip_news: bool = False
    skip_reprompt: bool = False
    authorise_key: str = Field("y", env="AUTHORISE_COMMAND_KEY")
    exit_key: str = Field("n", env="EXIT_KEY")
    noninteractive_mode: bool = False
    chat_messages_enabled: bool = Field(True, env="CHAT_MESSAGES_ENABLED")

    tts_config: TTSConfig = Field(default_factory=TTSConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    workspace_backend: FileWorkspaceBackendName = Field(
        FileWorkspaceBackendName.LOCAL, env="WORKSPACE_BACKEND"
    )

    continuous_mode: bool = False
    continuous_limit: int = 0

    memory_backend: str = Field("json_file", env="MEMORY_BACKEND")
    memory_index: str = Field("auto-gpt-memory", env="MEMORY_INDEX")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_password: str = Field("", env="REDIS_PASSWORD")
    wipe_redis_on_start: bool = Field(True, env="WIPE_REDIS_ON_START")

    disabled_command_categories: list[str] = Field(
        default_factory=list, env="DISABLED_COMMAND_CATEGORIES"
    )

    restrict_to_workspace: bool = Field(True, env="RESTRICT_TO_WORKSPACE")
    allow_downloads: bool = False

    shell_command_control: Literal["denylist", "allowlist"] = Field(
        "denylist", env="SHELL_COMMAND_CONTROL"
    )
    execute_local_commands: bool = Field(False, env="EXECUTE_LOCAL_COMMANDS")
    shell_denylist: list[str] = Field(
        default_factory=lambda: ["sudo", "su"], env="SHELL_DENYLIST"
    )
    shell_allowlist: list[str] = Field(
        default_factory=list, env="SHELL_ALLOWLIST"
    )

    image_provider: Optional[str] = Field(None, env="IMAGE_PROVIDER")
    huggingface_image_model: str = Field("CompVis/stable-diffusion-v1-4", env="HUGGINGFACE_IMAGE_MODEL")
    sd_webui_url: Optional[str] = Field(None, env="SD_WEBUI_URL")
    image_size: int = Field(256, env="IMAGE_SIZE")

    audio_to_text_provider: Literal["huggingface"] = Field("huggingface", env="AUDIO_TO_TEXT_PROVIDER")
    huggingface_audio_to_text_model: Optional[str] = Field(None, env="HUGGINGFACE_AUDIO_TO_TEXT_MODEL")

    selenium_web_browser: Literal["chrome", "firefox"] = Field("chrome", env="USE_WEB_BROWSER")
    selenium_headless: bool = Field(True, env="HEADLESS_BROWSER")
    user_agent: str = Field(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",  # noqa: E501
        env="USER_AGENT",
    )

    plugins_dir: str = Field("plugins", env="PLUGINS_DIR")
    plugins_config: PluginsConfig = Field(default_factory=PluginsConfig)
    plugins_allowlist: list[str] = Field(
        default_factory=list, env="ALLOWLISTED_PLUGINS"
    )
    plugins_denylist: list[str] = Field(
       
