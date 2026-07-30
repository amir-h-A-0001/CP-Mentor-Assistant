from dataclasses import dataclass, field
from typing import Optional
from .participant import ParticipantResult

@dataclass
class Contest:
    name: str
    platform: str
    number_of_problems: int
    duration: int
    participants: list[ParticipantResult] = field(default_factory=list)