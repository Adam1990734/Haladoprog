from dataclasses import dataclass
from pathlib import Path
import pathlib

@dataclass
class Configs:
    INPUT = Path(__file__).resolve().parent / "input"
    OUTPUT = Path(__file__).resolve().parent / "output"