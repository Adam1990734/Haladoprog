from enum import Enum

class CensorMode(str, Enum):
    BEEP: str = "BEEP"
    MUTE: str = "MUTE"