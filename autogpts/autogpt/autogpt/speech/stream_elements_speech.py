import os
import logging
import requests
import playsound  # type: ignore
from typing import Annotated, Callable, Optional

from autogpt.core.configuration import SystemConfiguration, UserConfigurable
from autogpt.speech.base import VoiceBase

try:
    from streamelements import SpeechClient  # type: ignore
except ImportError:
    SpeechClient = None  # type: Optional[Callable]

logger = logging.getLogger(__name__)


class StreamElementsConfig(SystemConfiguration):
    voice: str = UserConfigurable(default="Brian", from_env="STREAMELEMENTS_VOICE")


class StreamElementsSpeech(VoiceBase):
    """Streamelements speech module for autogpt"""

    def __init__(self, config: StreamElementsConfig):
        self.config = config

    def _speech(self, text: str, voice: str) -> bool:
        if SpeechClient is None:
            logger.error("The streamelements module is not installed.")
            return False

        voice = self.config.voice
        tts_url = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={text}"

        try:
            response = requests.get(tts_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Request failed with error: %s", e)
            return False

        try:
            with open("speech.mp3", "wb") as f:
                f.write(response.content)
        except Exception as e:
            logger.error("Failed to write speech.mp3 file: %s", e)
           
