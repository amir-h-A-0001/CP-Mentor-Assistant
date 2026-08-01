from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProblemResult:
    reject_count: int = 0
    accept_time: Optional[int] = None

    @property
    def is_solved(self):
        return self.accept_time is not None

    @property
    def tried(self):
        return self.reject_count > 0 or self.accept_time is not None