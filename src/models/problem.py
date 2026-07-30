from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProblemResult:
    reject_count: int = 0
    accept_time: Optional[int] = None

    @property
    def is_solved(self):
        return not self.accept_time is None