from dataclasses import dataclass

@dataclass
class Config:
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"

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