from enum import Enum

class CensorMode(str, Enum):
    BEEP: str = "beep"
    MUTE: str = "mute"