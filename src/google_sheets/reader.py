from . import spreadsheet

def check_sheets(sheet):
    required_worksheets = ['Participants','Contests','Main']
    existing_worksheets = {ws.title for ws in sheet.worksheets()}
    return all(ws in existing_worksheets for ws in required_worksheets)

def get_participant_names(sheet):
    ws = sheet.worksheet('Participants')
    return ws.col_values(1)[1:]

def get_participant_ids(sheet, platform_idx):
    ws = sheet.worksheet('Participants')
    return ws.col_values(platform_idx)[1:]

def get_platforms(sheet):
    ws = sheet.worksheet('Participants')
    return ws.row_values(1)[1:]

def get_number_of_recorded_contests(sheet):
    ws = sheet.worksheet('All')
    return (ws.col_count() - 2) // 2

def get_number_of_contests(sheet):
    ws = sheet.worksheet('All')
    return len(ws.col_values(3)) - 1

def get_contest_names(sheet):
    ws = sheet.worksheet('Contests')
    return ws.col_values(2)[1:]

def get_contest_short_names(sheet):
    ws = sheet.worksheet('Contests')
    return ws.col_values(4)[1:]

def get_all_contests(sheet):
    ws = sheet.worksheet('Contests')

    i = 2
    limit = ws.row_count()

    data = []

    if i <= limit:
        c_data = ws.row_values(i)
    else:
        return data

    while c_data:
        if len(c_data) != 5 or (not c_data[1]):
            data.append({})
        else:
            data.append(
                {
                    'name':c_data[1],
                    'weight':float(c_data[2]) if c_data[2] else 1,
                    'short_name': c_data[3] if c_data[3] else "c_" + str(i),
                    'url': c_data[4]
                }
            )
        i += 1
        if i <= limit:
            c_data = c_data = ws.row_values(i)
        else:
            break

    return data

def get_contest_weights(sheet):
    ws = sheet.worksheet('Contests')
    return [float(x) for x in  ws.col_values(3)[1:]]

def get_all_results(sheet):

    ws = sheet.worksheet('All')

    rows = ws.row_count() - 2
    cols = (ws.col_count() - 2) // 2

    contests_row = ws.row_values(1)[1:-1]

    data = {
        'contests': [contests_row[i * 2] for i in range(len(contests_row) // 2)],
        'results':{
            row[0]:
            [[int(row[1+j*2]) if row[1+j*2] and row[1+j*2] != '-' else row[1+j*2] ,
              int(row[1+j*2+1]) if row[1+j*2+1] else row[1+j*2+1]]
              for j in range(cols)]
            for row in [ws.row_values(i) for i in range(3,rows + 3)]
        }
    }

    absences = ws.col_values(len(data['contests'] * 2 + 2))[2:]

    for i,row in enumerate(data['results']):
        row.append(absences[i])

    return data