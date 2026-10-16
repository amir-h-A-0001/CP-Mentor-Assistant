from . import styler, spreadsheet, writer, reader
from src.models import *


def remove_standings(sheet, exception_list = None):
    """
    :param exception_list: list of short contest names
    """

    if exception_list is None:
        exception_list = []

    exception_list.extend(['Participants', 'Contests', 'Main'])

    for worksheet in sheet.worksheets():
        if worksheet.title not in exception_list:
            sheet.del_worksheet(worksheet)


def create_participants_list_page(sheet, rows: int):

    worksheet = sheet.add_worksheet("Participants", rows, 5)

    styler.prepare_participants_ws(worksheet)

    writer.write_participants_list_header(worksheet)

    return worksheet


def create_contests_list_page(sheet, rows: int):

    worksheet = sheet.add_worksheet("Contests", rows, 5)

    styler.prepare_contests_list_ws(worksheet)
    worksheet.update(
            range_name="A1:E1",
            values=[["Date", "Contest Name", "Weight", "Short Name", "URL"]]
        )

    return worksheet


def create_contest_standings_page(sheet, contest: Contest, name_dict, short_name : str):

    rows = 3 * len(contest.participants) + 2
    
    worksheet = sheet.add_worksheet(short_name, rows, 7 + contest.number_of_problems)

    styler.prepare_contest_standings_ws(worksheet, short_name, contest.problem_indices)
    
    writer.write_standings_header(worksheet,contest.problem_indices)
    
    current_row = 3
    for i, participant in enumerate(contest.participants):

        judge_result = [1 if p.is_solved else -1 if p.tried else 0 for p in participant.problems]
        styler.prepare_contest_standing_row(worksheet, current_row, judge_result )

        name = name_dict[participant.username]
        writer.write_standings_row(worksheet, participant, name, i, current_row)

        current_row += 3
       
    return worksheet


def create_all_results_page(sheet, data: dict):

    rows = len(data['results'])
    columns = len(data['contests'])

    worksheet = sheet.add_worksheet("All", 2 + rows, 2 + columns * 2 )

    styler.prepare_results_page(worksheet, rows, columns, final=False)

    writer.write_results_header(worksheet, columns, is_final= False)

    writer.write_absence_column(worksheet, rows, columns)
    
    writer.write_results(worksheet, data, has_header=False)

    return worksheet

def does_url_exist(sheet, url:str):

    contests = reader.get_all_contests(sheet)

    for contest in contests:
        if contest and contest['url'] == url:
            return True

    return False

def add_contest_to_all(sheet, contest_name:str, data: list):

    worksheet = sheet.worksheet('All')
    
    insert_col = worksheet.col_count()
    cols = reader.get_number_of_recorded_contests(sheet)
    rows = len(reader.get_participant_names(sheet))
    
    worksheet.add_cols(2)

    styler.insert_contest_result_col(worksheet, worksheet.row_count(),insert_col)

    worksheet.clear(
        start_row=3,
        end_row=worksheet.row_count(),
        start_col=insert_col,
        end_col=insert_col,
    )

    worksheet.update(
        row=2,
        col=insert_col,
        values=[["Performance","Solve"]]
    )

    writer.write_absence_column(worksheet, rows, cols + 1)

    writer.write_contest_col(worksheet,insert_col,contest_name,data)

def append_rows_to_all(sheet : spreadsheet.GoogleSpreadSheet, names):

    worksheet = sheet.worksheet('All')    

    last_row_index = worksheet.row_count()
    absence_col_index = worksheet.col_count()
    new_rows_count = len(names)

    worksheet.add_rows(new_rows_count)

    worksheet.copy_formula_request(
        source_start_row= last_row_index,
        source_end_row=last_row_index,
        source_start_col=absence_col_index,
        source_end_col=absence_col_index,
        
        dest_start_row=last_row_index+1,
        dest_end_row=last_row_index + new_rows_count,
        dest_start_col=absence_col_index,
        dest_end_col=absence_col_index 
    )

    names = [[name] for name in names]

    worksheet.update(
        row=last_row_index + 1,
        col= 1,
        values= names
    )


def create_final_results_page(sheet, title:str, rows: int, columns: int, data:dict):
    '''
    data must be formatted as:
        {
        'contests': list of contests
        'results': {
                username: list of result pairs 
            }
        }
    '''
    
    worksheet = sheet.add_worksheet(title, 3 + rows, 3 + columns * 2 )
    
    styler.prepare_results_page(worksheet, rows, columns, final=True)

    writer.write_results_header(worksheet, columns, is_final=True)

    worksheet.update(
        range_name="B1",
        values=[[title]]
    )

    writer.write_results(worksheet, data, has_header=True)

    return worksheet

def append_contest_info(sheet, short_name, url, contest, weight=None):

    last_row = len(reader.get_contest_names(sheet)) + 1

    worksheet = sheet.worksheet('Contests')

    writer.write_contest_info(
        worksheet,
        row=last_row+1,
        short_name=short_name,
        url=url,
        contest=contest,
        weight=weight
    )