from . import api, calculator
from src.models import *
import re

def extract_official(participants_set,contestID):

    data = api.get_standings(contestID)

    indices = [problem["index"] for problem in data["problems"]]

    participants_results = []

    for row in data["rows"]:
        username = row["party"]["members"][0]["handle"]

        if username in participants_set:

            problems = []
            solved = 0

            for i,problem in enumerate(row["problemResults"]):
                is_accepted = problem["points"] > 0
                problems.append(ProblemResult(
                    reject_count=problem["rejectedAttemptCount"],
                    accept_time=problem["bestSubmissionTimeSeconds"] if is_accepted else None
                )
                )
                solved += is_accepted

            p_res = ParticipantResult(
                username=username,
                performance=None,
                rank=row["rank"],
                solved=solved,
                penalty=row["penalty"],
                problems=problems
            )

            participants_results.append(p_res)

    return Contest(
        name=data["contest"]["name"],
        number_of_problems= len(data["problems"]),
        problem_indices= indices,
        participants=participants_results
    )


def get_performances(participants_set,contestID):

    rating_data = api.get_rating_changes(contestID)
    standing_data = api.get_standings(contestID)

    standings_by_handle = {
        row["party"]["members"][0]["handle"]: row
        for row in standing_data["rows"]
    }

    all_contestants = []

    for r_row in rating_data:
        handle = r_row["handle"]
        if handle not in standings_by_handle:
            continue
        s_row = standings_by_handle[handle]

        all_contestants.append(
            calculator.CF_Contestant(
                handle=handle,
                rating=r_row["oldRating"],
                points=s_row["points"],
                penalty=s_row["penalty"],
            )
        )

    return calculator.calc(all_contestants,participants_set)


def get_contest_id(url: str) -> int:
    match = re.search(r'codeforces\.com/contest/(\d+)', url)

    if not match:
        raise ValueError("Invalid Codeforces contest URL")

    return int(match.group(1))


def get_contest_results(participants_set, url, include_virtual=False):

    contestID = get_contest_id(url)

    result = extract_official(participants_set, contestID)
    performances = get_performances(participants_set, contestID)

    for participant in result.participants:
        participant.performance = performances[participant.username]

    # TODO add virtuals

    return result