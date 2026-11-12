from dataclasses import dataclass

@dataclass
class Config:
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"

    TILTOTT_SZAVAK = [
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