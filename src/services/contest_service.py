from src.google_sheets import services, reader
import src.platforms as platforms
import src.models

def add_contest(sheet, short_title, url, include_virtuals, platform_name=None, weight=None):

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
    services.append_contest_info(sheet, short_title, url, contest, weight)


def create_final_table(sheet, *, title, number_of_contests, most_absences, best_first, weighted):

    data = reader.get_all_results(sheet)

    number_of_contests = min(number_of_contests,len(data['contests']))

    # Remove participants with absences exceeding the limit + remove absence count
    data['results'] = {k:v[:-1] for k,v in data['results'] if v[-1] <= most_absences}

    # Replace solve count with contest index
    for row in data['results'].values():
        for i,pair in enumerate(row):
            pair[1] = i + 1

    # Sort and choose the best contests based on the performance
    if(best_first):
        for row in data['results'].values():
            row.sort(key=lambda x: x[0] if (x[0] != '' and x[0] != '-') else 0, reverse=True)
    
    # Slice the number of wanted contests
    for row in data['results'].values():
        row = row[:number_of_contests]

    # Read weights from contests page and Calculate weighted sum and weighted average or mean if weightd was False
    weights = reader.get_contest_weights(sheet) if weighted else ([1]* len(data['contests']))

    for row in data['results'].values():
        weighted_sum = sum([pair[0] * weights[pair[1]-1] if (pair[0] != '' and pair[0] != '-') else 0 for pair in row])
        weights_sum = sum([weights[pair[1]-1] if pair[1] else 0 for pair in row])
        row.append(
            [weighted_sum, weighted_sum / weights_sum]
        )

    # Sort participants based on their personal rating
    data['results'] = dict(sorted(
        data['results'].items(),
        key=lambda x: x[1][number_of_contests][1],
        reverse=True
    ))

    # Write the results in a new worksheet
    return services.create_final_results_page(
        sheet,
        title=title,
        rows=len(data['results']),
        columns=len(data['contests']),
        data=data
    )
