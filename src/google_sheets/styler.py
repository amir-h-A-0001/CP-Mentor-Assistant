import json
import gspread
from . import spreadsheet 

def clear_all(sheet):
    try:
        sheet.worksheet("Note")
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(
            title="Note",
            rows=100,
            cols=20
        )

    for worksheet in sheet.worksheets():
        if worksheet.title != "Note":
            sheet.del_worksheet(worksheet)


def create_participants_ws(sheet):

    ws = sheet.add_worksheet("Participants", 1000, 5)
    requests = []

    requests.append(
        ws.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
    ))

    requests.append(
        ws.update_column_width_request(
            start_col=1,
            end_col=1,
            width=214
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=2,
            end_col=3,
            width=130
        )
    )

    requests.append(
        ws.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        ws.center_sheet_request()
    )

    requests.append(
        ws.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            color=(224.95,224.95,224.95)
        )
    )

    ws.send_batch_request(requests)

    # ws.update(
    #     range_name="A1:C1",
    #     values=[["FullName", "CF ID", "AtCoder ID"]]
    # )



def create_contests_list_ws(sheet):

    ws = sheet.add_worksheet("Contests", 200, 5)
    requests = []

    requests.append(
        ws.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
    ))

    requests.append(
        ws.update_column_width_request(
            start_col=1,
            end_col=1,
            width=144
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=2,
            end_col=2,
            width=340
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=3,
            end_col=3,
            width=70
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=4,
            end_col=4,
            width=130
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=5,
            end_col=5,
            width=65
        )
    )

    requests.append(
        ws.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        ws.center_sheet_request()
    )

    requests.append(
        ws.format_date_column_request(
            column=1
        )
    )

    requests.append(
        ws.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            color=(224.95,224.95,224.95)
        )
    )

    ws.send_batch_request(requests)

    # ws.update(
    #     range_name="A1:E1",
    #     values=[["Date", "Contest Name", "Weight", "Short Name", "URL"]]
    # )


def create_contest_ws(sheet, short_name, indices):

    problems_count = len(indices)
    ws = sheet.add_worksheet(short_name, 500, 6 + problems_count)
    requests = []

    requests.append(
        ws.center_sheet_request()
        )

    requests.append(
        ws.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=1,
            end_col=1,
            width=214
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=2,
            end_col=2,
            width=55
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=3,
            end_col=3,
            width=60
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=4,
            end_col=4,
            width=5
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=5,
            end_col=5-1 + problems_count,
            width=62
        )
    )

    split = 5 + problems_count
    requests.append(
        ws.update_column_width_request(
            start_col=split,
            end_col=split,
            width=5
        )
    )

    requests.append(
        ws.update_column_width_request(
            start_col=split+1,
            end_col=split+1,
            width=100
        )
    )

    requests.append(
        ws.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=split+1,
            color=(239, 239, 239)
        )
    )

    requests.append(
        ws.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=4,
            end_col=4,
            color=(153,153,153)
        )
    )

    requests.append(
        ws.update_frozen_request(
            frozen_rows=1,
            frozen_columns=1
        )
    )

    requests.append(
        ws.update_row_height_request(
            start_row=2,
            end_row=2,
            height=8
        )
    )

    requests.append(
        ws.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=split+1,
            fontFamily="Lexend"
        )
    )

    ws.send_batch_request(requests)

    # ws.update(
    #     range_name="A1",
    #     values=[["Contestant", "Solved", "Penalty", ""] + indices + ["", "Performance"]]
    # )


def _accepted_cell_style(ws, row, col):
    requests = []

    requests.append(
        ws.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=col,
            end_col=col,
            color=(217,234,211)
        )
    )

    requests.append(
        ws.update_font_request(
            start_row=row,
            end_row=row,
            start_col=col,
            end_col=col,
            bold= True,
            color=(56,118,29)
        )
    )

    return requests

def _rejected_cell_style(ws, row, col):
    requests = []

    requests.append(
        ws.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=col,
            end_col=col,
            color=(244,204,204)
        )
    )

    requests.append(
        ws.update_font_request(
            start_row=row,
            end_row=row,
            start_col=col,
            end_col=col,
            bold=True,
            color=(204,0,0)
        )
    )

    return requests

def prepare_contest_standing_row(contest_worksheet, row, judge_results):

    problems_count = len(judge_results)
    requests = []

    requests.append(
        contest_worksheet.update_row_height_request(
            start_row=row,
            end_row=row,
            height=36
        )
    )

    requests.append(
        contest_worksheet.update_row_height_request(
            start_row=row+1,
            end_row=row+1,
            height=23
        )
    )

    requests.append(
        contest_worksheet.update_row_height_request(
            start_row=row+2,
            end_row=row+2,
            height=8
        )
    )

    requests.append(
        contest_worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=1,
            end_col=1,
            color=(204,204,204)
        )
    )

    requests.append(
        contest_worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=2,
            end_col=3,
            color=(217,217,217)
        )
    )

    requests.append(
        contest_worksheet.update_font_request(
            start_row=row,
            end_row=row+1,
            start_col=1,
            end_col=3,
            fontFamily="Lexend"
        )
    )

    requests.append(
        contest_worksheet.update_font_request(
            start_row=row+1,
            end_row=row+1,
            start_col=1,
            end_col=3,
            color=(102,102,102)
        )
    )

    requests.append(
        contest_worksheet.update_range_color_request(
            start_row=row+1,
            end_row=row,
            start_col=4,
            end_col=4,
            color=(153,153,153)
        )
    )


    start_col = 5
    requests.append(
        contest_worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=5,
            end_col=start_col + problems_count + 1,
            color=(239,239,239)
        )
    )

    requests.append(
        contest_worksheet.update_font_request(
            start_row=row+1,
            end_row=row+1,
            start_col=start_col,
            end_col=start_col + problems_count - 1,
            color=(67,67,67)
        )
    )

    for i,res in enumerate(judge_results):
        if res == 0:
            continue

        cell_style = _accepted_cell_style if res > 0 else _rejected_cell_style
        requests.extend(cell_style(contest_worksheet, row,start_col+i))

    contest_worksheet.send_batch_request(requests)
