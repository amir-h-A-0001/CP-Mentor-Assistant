import google_sheets as gs
import models

def add_contest_to_all(sheet, platform_idx, contest):


    # CONVERT LOGIC
    usernames = gs.reader.get_participant_ids(sheet, platform_idx)
    
    participant_map = {
        p.username: p
        for p in contest.participants
    }

    participants_ordered = [
        [participant_map[name]] if name in participant_map else []
        for name in usernames
    ]

    data = [[c.performance, c.solved] for c in participants_ordered]

    # -------------