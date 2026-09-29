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

def get_number_of_contests(sheet):
    ws = sheet.worksheet('All')
    return (ws.col_count() - 2) // 2

def get_contest_names(sheet):
    ws = sheet.worksheet('Contests')
    return ws.col_values(2)[1:]

def get_contest_short_names(sheet):
    ws = sheet.worksheet('Contests')
    return ws.col_values(4)[1:]

def get_contest_weights(sheet):
    ws = sheet.worksheet('Contests')
    return [float(x) for x in  ws.col_values(3)[1:]]

def get_all_results(sheet):

    ws = sheet.worksheet('All')

    rows = ws.row_count() - 2
    cols = (ws.col_count() - 2) // 2

    contests_row = ws.row_values(1)[1:-1]

    return {
        'contests': [contests_row[i * 2] for i in range(len(contests_row) // 2)],
        'results':{
            row[0]:
            [[int(row[1+j*2]) if row[1+j*2] else row[1+j*2] ,
              int(row[1+j*2+1]) if row[1+j*2+1] else row[1+j*2+1]]
              for j in range(cols)]
            for row in [ws.row_values(i) for i in range(3,rows + 3)]
        }
    }
