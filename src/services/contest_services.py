from src.google_sheets import services, reader
import src.platforms as platforms
import src.models

    # TODO : check existance based on ID

def add_contest(sheet, short_title, url, include_virtuals, create_standings, exists=False, platform_name=None, weight=None):

    # Find the platform
    if platform_name is not None:
        platform = platforms.get_platform(platform_name)
    else:
        platform = platforms.get_platform_from_url(url)

    if not exists and services.is_contest_recorded(sheet, url):
            return "Already exists"

    # Extract name and usernames and connect them
    names = reader.get_participant_names(sheet)
    usernames = reader.get_participant_ids(sheet, platform.USERNAME_COLUMN)

    names_dict = {
        username : name 
        for username,name in zip(usernames, names)
    }

    # Prepare participants format and exract contest data
    participants_set = set(usernames)
    contest = platform.extract(participants_set, url, include_virtuals)

    # Create standings page
    if create_standings and short_title in sheet.worksheets():
        services.create_contest_standings_page(sheet, contest, names_dict, short_title)

    # Prepare format for all results page and add contest to the page
    participant_map = {
        p.username: p
        for p in contest.participants
    }

    participants_ordered = [
        participant_map[name] if name in participant_map else None
        for name in usernames
    ]

    data = [[c.performance if c.performance > 0 else '-', c.solved] if c else [] for c in participants_ordered]
    data.append([platform.get_code(url)])
    services.add_contest_to_all(sheet, contest.name, data)

    # Add contest to the contests page
    if not exists:
        services.append_contest_info(sheet, short_title, url, contest, weight)

    return "Done"


def add_batch_contests(sheet, include_virtuals, create_standings):

    result_log = []

    contests = reader.get_all_contests(sheet)
    # recorded = reader.get_number_of_recorded_contests(sheet)

    for i,c in enumerate(contests):
        
        if not c:
            result_log.append((False, f'Insufficient data for row {i + 2} (name and url are mandatory)'))
            continue

        add_contest(
            sheet=sheet,
            short_title=c['short_name'],
            url=c['url'],
            include_virtuals=include_virtuals,
            create_standings=create_standings,
            exists=True
        )
     
        result_log.append((True,f'{c['name']} was added from row {i + 1})'))

    return result_log
    

