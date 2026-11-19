from dataclasses import dataclass

@dataclass
class ProfanityMatch:
    word: str
    start: float
    end: float