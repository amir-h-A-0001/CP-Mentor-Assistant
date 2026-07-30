from dataclasses import dataclass
from functools import cmp_to_key
import math


@dataclass
class Contestant:
    handle: str
    rating: int
    points: float
    penalty: int

    rank: int = 0
    seed: float = 0.0
    need_rating: int = 0
    delta: int = 0
    performance: int = 0


mem_ranks = [0.0] * 8001


def get_elo_win_probability(ra: int, rb: int) -> float:
    return 1.0 / (1.0 + math.pow(10.0, (rb - ra) / 400.0))


def get_seed(contestants: list[Contestant], rating: int) -> float:
    if mem_ranks[rating] == 0:
        seed = 1.0

        for contestant in contestants:
            seed += get_elo_win_probability(contestant.rating, rating)

        mem_ranks[rating] = seed

    return mem_ranks[rating]


def get_rating_to_rank(contestants: list[Contestant], rank: float) -> int:
    left = 1
    right = 8000

    while right - left > 1:
        mid = (left + right) // 2

        if get_seed(contestants, mid) < rank:
            right = mid
        else:
            left = mid

    return left


def compare_contestants(ca: Contestant, cb: Contestant):
    if ca.points == cb.points:
        return cb.penalty - ca.penalty

    return ca.points - cb.points


def reassign_ranks(contestants: list[Contestant]):
    contestants.sort(
        key=cmp_to_key(lambda a, b: -compare_contestants(a, b))
    )

    first = 0

    for i in range(1, len(contestants)):
        if compare_contestants(contestants[first], contestants[i]) != 0:
            for j in range(first, i):
                contestants[j].rank = i
            first = i

    for i in range(first, len(contestants)):
        contestants[i].rank = len(contestants)


def adjust_rating_changes(contestants: list[Contestant]):
    contestants.sort(key=lambda c: c.rating, reverse=True)

    all_sum = 0

    for contestant in contestants:
        all_sum += contestant.delta

    all_inc = math.trunc(-all_sum / len(contestants)) - 1

    for contestant in contestants:
        contestant.delta += all_inc

    top_count = min(
        len(contestants),
        4 * math.floor(math.sqrt(len(contestants)) + 0.5)
    )

    top_sum = 0

    for contestant in contestants[:top_count]:
        top_sum += contestant.delta

    top_inc = min(
        max(math.trunc(-top_sum / top_count), -10),
        0,
    )

    for contestant in contestants[:top_count]:
        contestant.delta += top_inc

    contestants.sort(key=lambda c: c.rank)


def predict_rating_changes(contestants: list[Contestant]) -> list[Contestant]:
    global mem_ranks

    mem_ranks = [0.0] * 8001

    reassign_ranks(contestants)

    for contestant in contestants:
        contestant.seed = get_seed(contestants, contestant.rating) - 0.5

        mid_rank = math.sqrt(contestant.rank * contestant.seed)

        contestant.need_rating = get_rating_to_rank(
            contestants,
            mid_rank,
        )

        contestant.delta = math.trunc(
            (contestant.need_rating - contestant.rating) / 2
        )

        contestant.performance = get_rating_to_rank(
            contestants,
            contestant.rank,
        )

    adjust_rating_changes(contestants)

    return contestants



def calc(contestants: list[Contestant], handles: list[str] | None = None) -> dict[str, int]:
    """
    Calculates the performance rating for contestants.

    Args:
        contestants: All rated contestants in the contest.
        handles: Handles whose performance should be returned.
                 If None, returns the performance for everyone.

    Returns:
        Dictionary mapping handle -> performance.
    """

    # TODO:
    # contestants must contain EVERY rated contestant in the contest.
    # Each Contestant must have:
    #   - handle
    #   - rating (old rating before the contest)
    #   - points (official Codeforces points, NOT necessarily solved count)
    #   - penalty
    


    predict_rating_changes(contestants)

    if handles is None:
        return {
            contestant.handle: contestant.performance
            for contestant in contestants
        }

    handles = set(handles)

    return {
        contestant.handle: contestant.performance
        for contestant in contestants
        if contestant.handle in handles
    }