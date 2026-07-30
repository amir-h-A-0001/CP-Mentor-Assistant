import requests
import json
from . import api
from src.models import *

def extract_official(participants,contestID):

    data = api.get_standings(contestID)
    participants_results = []

    for row in data["rows"]:
        username = row["party"]["members"][0]["handle"]

        if username in participants:

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
        platform="Codeforces",
        number_of_problems= len(data["problems"]),
        duration=data["contest"]["durationSeconds"],
        participants=participants_results
    )
