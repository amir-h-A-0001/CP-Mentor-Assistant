from . import styler, spreadsheet
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
    worksheet.update(
        range_name="A1:C1",
        values=[["FullName", "CF ID", "AtCoder ID"]]
    )

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
    worksheet.update(
            range_name="A1",
            values=[["Rank", "Contestant", "Solved", "Penalty", ""] + contest.problem_indices + ["", "Performance"]]
        )

    current_row = 3
    for i, participant in enumerate(contest.participants):

        judge_result = [1 if p.is_solved else -1 if p.tried else 0 for p in participant.problems]
        styler.prepare_contest_standing_row(worksheet, current_row, judge_result )

        solved = 0
        attempts = 0
        for p in participant.problems:
            if p.tried:
                attempts += p.reject_count
            if p.is_solved:
                solved += 1
                attempts += 1

        penalty_s = participant.penalty

        hours = penalty_s // 60
        minutes = (penalty_s % 60)

        first_row = (
            [participant.rank, name_dict[participant.username], solved, penalty_s, '']
            + [
                '' if not p.tried else f"{p.reject_count}{'+' if p.is_solved else '-'}"
                for p in participant.problems
            ]
            + ['', participant.performance]
        )

        second_row = (
            [i+1, participant.username, attempts, f"{hours}:{minutes:02d}", '']
            + [
                '' if not p.is_solved else (f"{p.accept_time // 3600}:{((p.accept_time % 3600)//60):02d}") for p in participant.problems
            ]
            + ['','']
        )

        worksheet.update(
            row=current_row,
            col=1,
            values=[first_row, second_row],
        )

        current_row += 3
       
    return worksheet


def create_final_results_page(sheet, data):
    ...

# data retreival

def get_participant_names(sheet):
    ws = sheet.worksheet('Participants')
    return ws.col_values(1)[1:]

def get_participant_ids(sheet, col):
    ws = sheet.worksheet('Participants')
    return ws.col_values(col)[1:]

def get_platforms(sheet):
    ws = sheet.worksheet('Participants')
    return ws.row_values(1)[1:]

def get_final_results(sheet):
    ...

        
