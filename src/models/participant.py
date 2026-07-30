from dataclasses import dataclass, field
from typing import Optional
from .problem import ProblemResult

@dataclass
class ParticipantResult:
    username: str
    performance: int
    rank: int
    solved: int
    penalty: int
    problems: list[ProblemResult] = field(default_factory=list)

    @property
    def problems_count(self):
        return len(self.problems)

    @property
    def virtual(self):
        return not self.virtual is None