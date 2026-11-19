from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    INPUT_DIR = os.path.join(str(Path(__file__).resolve().parent), "input")
    OUTPUT_DIR = os.path.join(str(Path(__file__).resolve().parent), "output")
    TEMP_DIR = os.path.join(str(Path(__file__).resolve().parent), "temp")

    ASR_MODEL = "openai/whisper-small"

    PROFANITY_MODEL = "tarekziade/pardonmyai"

    PROFANITY_LABEL = "LABEL_1"

    PROFANITY_THRESHOLD = 0.30

    FORBIDDEN_WORDS = [
        "fuck",
        "fucking",
        "fucker",
        "shit",
        "bitch",
        "asshole",
        "bastard",
        "dick",
        "cunt",
        "stupid"
    ]

print(Config.INPUT_DIR)