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


def create_contest_standings_page(sheet, contest: Contest, name_dict, short_name : str, rows: int):

    worksheet = sheet.add_worksheet(short_name, rows, 7 + contest.number_of_problems)

    styler.prepare_contest_standings_ws(worksheet, short_name, contest.problem_indices)
    
    writer.write_standings_header(worksheet,contest.problem_indices)

    writer.write_standings(worksheet, contest.participants, name_dict)
    
    current_row = 3
    for i, participant in enumerate(contest.participants):

        judge_result = [1 if p.is_solved else -1 if p.tried else 0 for p in participant.problems]
        styler.prepare_contest_standing_row(worksheet, current_row, judge_result )

        username = name_dict[participant.username]
        writer.write_standings_row(worksheet, participant, username, i, current_row)

        current_row += 3
       
    return worksheet


def create_all_results_page(sheet, rows: int, columns: int, data: dict):

    worksheet = sheet.add_worksheet("All", 2 + rows, 2 + columns * 2 )

    styler.prepare_results_page(worksheet, rows, columns, final=False)

    writer.write_results_header(worksheet, columns, is_final= False)

    writer.write_absence_column(worksheet, rows, columns)
    
    writer.write_results(worksheet, data, has_header=False)

    return worksheet


def add_contest_to_all(sheet, contest_name:str, data: list):

    worksheet = sheet.worksheet('All')
    
    insert_col = worksheet.col_count()
    cols = reader.get_number_of_contests(sheet)
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





    





def create_final_results_page(sheet, data):
    ...
