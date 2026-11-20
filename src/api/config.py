from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Configs:
    PUBLIC = os.path.join(Path(__file__).resolve().parent, "public")
    TEMPLATES = os.path.join(Path(__file__).parent, "public", "templates")

    INPUT = os.path.join(Path(__file__).resolve().parent.parent, "moduls", "input")
    OUTPUT = os.path.join(Path(__file__).resolve().parent.parent, "moduls", "output")

    CENSURE = os.path.join(Path(__file__).resolve().parent.parent, "moduls", "censor.py")