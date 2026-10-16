from src.google_sheets import services, reader

def create_final_table(sheet, *, title, number_of_contests, most_absences, best_first, weighted):

    data = reader.get_all_results(sheet)

    number_of_contests = min(number_of_contests,len(data['contests']))

    # Remove participants with absences exceeding the limit + remove absence count
    data['results'] = {k:v[:-1] for k,v in data['results'].items() if v[-1] <= most_absences}

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
