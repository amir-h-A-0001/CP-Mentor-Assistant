from src.google_sheets import services, reader
import src.models

def add_contest_to_all(sheet, platform_idx, contest):

    usernames = reader.get_participant_ids(sheet, platform_idx)
    
    participant_map = {
        p.username: p
        for p in contest.participants
    }

    participants_ordered = [
        [participant_map[name]] if name in participant_map else []
        for name in usernames
    ]

    data = [[c.performance, c.solved] for c in participants_ordered]

    services.add_contest_to_all(sheet, contest.name, data)



def create_final_table(sheet, *, title, number_of_contests, best_first, weighted):

    data = reader.get_all_results(sheet)

    for row in data['results'].values():
        for i,pair in enumerate(row):
            pair[1] = i + 1

    if(best_first):
        for row in data['results'].values():
            row.sort(key=lambda x: x[0] if x[0] != '' else 0, reverse=True)

    for row in data['results'].values():
        row = row[:min(number_of_contests,len(row))]

    weights = reader.get_contest_weights(sheet) if weighted else ([1]* len(data['contests']))

    for row in data['results'].values():
        weighted_sum = sum([pair[0] * weights[pair[1]-1] if pair[0] else 0 for pair in row])
        weights_sum = sum([weights[pair[1]-1] if pair[1] else 0 for pair in row])
        row.append(
            [weighted_sum, weighted_sum / weights_sum]
        )

    services.create_final_results_page(
        sheet,
        title=title,
        rows=len(data['results']),
        columns=len(data['contests']),
        data=data
    )


