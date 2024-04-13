""" GTTS Voice. """
from __future__ import annotations

import os
import subprocess
from gtts import gTTS
from gtts.utils import get_filename
from autogpt.speech.base import VoiceBase

class GTTSVoice(VoiceBase):
    """GTTS Voice."""

    def __init__(self):
        super().__init__()

    def _setup(self) -> None:
        pass

    def _speech(self, text: str, rate: int = 200) -> bool:
        """Play the given text."""
        tts = gTTS(text, lang="en", slow=False, tld="com.au", rate=rate)
        filename = get_filename(text)
        tts.save(filename)
        try:
            subprocess.run(["afplay", filename])
        except FileNotFoundError:
            print("afplay not found, install it to play audio.")
        finally:
            os.remove(filename)
        return True
