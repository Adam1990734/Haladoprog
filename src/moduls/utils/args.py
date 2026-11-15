from pathlib import Path
from models.censor_mode import CensorMode

def get_mode(args: list[str]) -> CensorMode:
    MODE = "--mode"

    if MODE not in args:
        raise ValueError("The mode is required!")

    mode = None

    try:
        mode = args[args.index(MODE) + 1]
    except:
        raise ValueError("You should always give one mode [BEEP, MUTE]!")
    
    if mode == "BEEP":
        return CensorMode.BEEP
    if mode == "MUTE":
        return CensorMode.MUTE

    raise ValueError("The given mode is not supported!")

def get_video_source(args: list[str]) -> Path:
    SOURCE = "--source"

    if SOURCE not in args:
        raise ValueError("The source is required!")

    source = None

    try:
        source = Path(
            args[args.index(SOURCE) + 1]
        )
    except:
        raise FileNotFoundError("You should always give one path!")

    if not source.exists():
        raise FileNotFoundError("The given source is not exists!")

    return source