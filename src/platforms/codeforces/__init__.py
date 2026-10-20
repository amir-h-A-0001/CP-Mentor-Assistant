from .adapter import get_contest_results as extract
from .adapter import get_code

USERNAME_COLUMN = 2

def supports(url: str) -> bool:
    return 'codeforces.com/contest' in url
