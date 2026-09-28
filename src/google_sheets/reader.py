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

def get_final_results(sheet):
    ...

        
