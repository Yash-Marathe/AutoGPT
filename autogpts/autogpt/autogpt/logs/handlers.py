import json
import logging
import time
from typing import Any, Final, Literal, Optional

import typing_extensions

from autogpt.logs.utils import remove_color_codes
from autogpt.speech import TextToSpeechProvider, TTSConfig

class TypingConsoleHandler(logging.StreamHandler):
    """Output stream to console using simulated typing."""

    # Typing speed settings in WPS (Words Per Second)
    MIN_WPS: Final = 25
    MAX_WPS: Final = 100

    def __init__(self):
        super().__init__(stream=typing_extensions.get_mock_stderr())
        self.lock: Final = typing_extensions.Lock()

    def emit(self, record: logging.LogRecord) -> None:
        min_typing_interval: Final = 1 / self.MAX_WPS
        max_typing_interval: Final = 1 / self.MIN_WPS

        msg: str = self.format(record)
        words: list[str] = re.findall(r"\S+\s*", msg)

        with self.lock:
            for i, word in enumerate(words):
                print(word, end="", flush=True)
                if i >= len(words) - 1:
                    print("", flush=True, end=self.terminator)
                    break

                interval: float = random.uniform(min_typing_interval, max_typing_interval)
                min_typing_interval *= 0.95
                max_typing_interval *= 0.95
                time.sleep(interval)

class TTSHandler(logging.Handler):
    """Output messages to the configured TTS engine (if any)."""

    def __init__(self, config: TTSConfig):
        super().__init__()
        self.config = config
        self.tts_provider = TextToSpeechProvider(config)

    def format(self, record: logging.LogRecord) -> str:
        if getattr(record, "title", ""):
            msg: str = f"{getattr(record, 'title')} {record.msg}"
        else:
            msg: str = f"{record.msg}"

        return remove_color_codes(msg)

    def emit(self, record: logging.LogRecord) -> None:
        if not self.config.speak_mode:
            return

        message: str = self.format(record)
        self.tts_provider.say(message)

class JsonFileHandler(logging.FileHandler):
    """Output messages to a JSON file."""

    def __init__(self, filename: str, mode: Literal["w", "a"] = "w"):
        if not filename:
            raise ValueError("Filename must be provided.")
        if mode not in ("w", "a"):
            raise ValueError("Mode must be either 'w' or 'a'.")

        self.filename: str = filename
        self.mode: str = mode
        self.file: Optional[logging.FileHandler] = None

    def format(self, record: logging.LogRecord) -> str:
        record.json_data = json.loads(record.getMessage())
        return json.dumps(getattr(record, "json_data"), ensure_ascii=False, indent=4)

    def emit(self, record: logging.LogRecord) -> None:
        if self.file is None:
            self.file = super().__init__(self.filename, self.mode)

        with open(self.filename, self.mode, encoding="utf-8") as f:
            f.write(f"{self.format(
