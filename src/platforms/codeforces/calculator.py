from dataclasses import dataclass
import math


@dataclass
class CF_Contestant:
    handle: str
    rating: int
    points: float
    penalty: int

    rank: int = 0
    seed: float = 0.0
    need_rating: int = 0
    delta: int = 0
    performance: int = 0


def _get_elo_win_probability(ra: float, rb: float) -> float:
    return 1.0 / (1.0 + 10.0 ** ((rb - ra) / 400.0))


def _get_seed(contestants: list[CF_Contestant], rating: int, memo: dict[int, float]) -> float:
    if rating not in memo:
        memo[rating] = 1.0 + sum(
            _get_elo_win_probability(c.rating, rating) for c in contestants
        )
    return memo[rating]


def _get_rating_to_rank(contestants: list[CF_Contestant], rank: float, memo: dict[int, float]) -> int:
    left, right = 1, 8000
    while right - left > 1:
        mid = (left + right) // 2
        if _get_seed(contestants, mid, memo) < rank:
            right = mid
        else:
            left = mid
    return left


def _reassign_ranks(contestants: list[CF_Contestant]) -> None:
    # Sort descending by points, ascending by penalty
    contestants.sort(key=lambda c: (-c.points, c.penalty))

    first = 0
    n = len(contestants)
    for i in range(1, n):
        # Tied if both points and penalty match
        if contestants[first].points != contestants[i].points or contestants[first].penalty != contestants[i].penalty:
            for j in range(first, i):
                contestants[j].rank = i
            first = i

    for j in range(first, n):
        contestants[j].rank = n


def _adjust_rating_changes(contestants: list[CF_Contestant]) -> None:
    contestants.sort(key=lambda c: c.rating, reverse=True)
    n = len(contestants)
    if n == 0:
        return

    all_sum = sum(c.delta for c in contestants)
    all_inc = int(-all_sum / n) - 1
    for c in contestants:
        c.delta += all_inc

    top_count = min(
        n,
        4 * math.floor(math.sqrt(n) + 0.5)
    )
    top_sum = sum(contestants[i].delta for i in range(top_count))
    top_inc = min(max(int(-top_sum / top_count), -10), 0)

    for i in range(top_count):
        contestants[i].delta += top_inc

    contestants.sort(key=lambda c: c.rank)


def calc(contestants: list[CF_Contestant], handles: set[str] | None = None) -> dict[str, int]:
    """
    Calculates the performance rating for contestants.

    Args:
        contestants: All rated contestants in the contest.
        handles: Handles whose performance should be returned.
                 If None, returns the performance for everyone.

    Returns:
        Dictionary mapping handle -> performance.
    """
    if not contestants:
        return {}

    # 1. Reassign ranks based on contest standings (points & penalty)
    _reassign_ranks(contestants)

    # 2. Compute seeds, need_rating, delta, and performance
    memo: dict[int, float] = {}

    for c in contestants:
        c.seed = _get_seed(contestants, c.rating, memo) - 0.5
        mid_rank = math.sqrt(c.rank * c.seed)
        c.need_rating = _get_rating_to_rank(contestants, mid_rank, memo)
        c.delta = int((c.need_rating - c.rating) / 2)
        c.performance = _get_rating_to_rank(contestants, c.rank, memo)

    # 3. Adjust rating changes (updates delta in-place)
    _adjust_rating_changes(contestants)

    # 4. Filter and return requested handles
    if handles is None:
        return {
            contestant.handle: contestant.performance - 400
            for contestant in contestants
        }

    handles_set = set(handles)

    return {
        contestant.handle: contestant.performance - 400
        for contestant in contestants
        if contestant.handle in handles_set
    }