from dataclasses import dataclass

@dataclass
class Token:
    token: str
    type: str
    line: int