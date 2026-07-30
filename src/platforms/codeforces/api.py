import requests

def get_standings(contestID):
    url = "https://codeforces.com/api/contest.standings"
    params = {
        "contestId": contestID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == 'FAILED':
        raise Exception(data["comment"])

    return data["result"]