from src.google_sheets import services, reader
import src.platforms as platforms
import src.models

def add_contest(sheet, short_title, url, include_virtuals, create_standings, exists=False, platform_name=None, weight=None):

    # Find the platform
    if platform_name is not None:
        platform = platforms.get_platform(platform_name)
    else:
        platform = platforms.get_platform_from_url(url)

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
    if create_standings:
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

    services.add_contest_to_all(sheet, contest.name, data)

    # Add contest to the contests page
    if not exists:
        services.append_contest_info(sheet, short_title, url, contest, weight)

def add_batch_contests(sheet, include_virtuals, create_standings):

    contests = reader.get_all_contests(sheet)
    recorded = reader.get_number_of_recorded_contests(sheet)

    for i,c in enumerate(contests):
        if i < recorded:
            continue

        if not c:
            print(f'Insufficient data for row {i + 2} (name and url are mandatory)')
            continue

        add_contest(
            sheet=sheet,
            short_title=c['short_name'],
            url=c['url'],
            include_virtuals=include_virtuals,
            create_standings=create_standings,
            exists=True
        )

