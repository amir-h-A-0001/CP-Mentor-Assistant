from dataclasses import dataclass, field
from typing import Optional
from .participant import ParticipantResult

@dataclass
class Contest:
    name: str
    number_of_problems: int
    problem_indices: list[str] = field(default_factory=list)
    participants: list[ParticipantResult] = field(default_factory=list)