import json
import gspread
from . import client 

# Text colors
RESET = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
BRIGHT = "\033[1m"
DIM    = "\033[2m"




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
    ws_id = ws.id

    print('[Participants] preparing style queries...\t')
    requests = []

    requests.append(client.update_row_height_request(
        sheet_id=ws_id,
        start_row=1,
        end_row=1,
        height=42
    ))

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=1,
            end_col=1,
            width=214
        )
    )

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=2,
            end_col=3,
            width=130
        )
    )

    requests.append(
        client.update_font_request(
            sheet_id=ws_id,
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        client.center_sheet_request(sheet_id=ws_id)
    )

    requests.append(
        client.update_range_color_request(
            sheet_id=ws_id,
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            color=(224.95,224.95,224.95)
        )
    )
    print(GREEN + 'Done\n' + RESET)

    print('[Participants] sending style queries...\t')
    client.send_batch_request(ws, requests)
    print()
    ws.update(
        range_name="A1:C1",
        values=[["FullName", "CF ID", "AtCoder ID"]]
    )



def create_contests_ws(sheet):
    ws = sheet.add_worksheet("Contests", 200, 5)
    ws_id = ws.id

    print('[Contests] preparing style queries...\t')
    requests = []

    requests.append(client.update_row_height_request(
        sheet_id=ws_id,
        start_row=1,
        end_row=1,
        height=42
    ))

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=1,
            end_col=1,
            width=144
        )
    )

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=2,
            end_col=2,
            width=340
        )
    )

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=3,
            end_col=3,
            width=70
        )
    )

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=4,
            end_col=4,
            width=130
        )
    )

    requests.append(
        client.update_column_width_request(
            sheet_id=ws_id,
            start_col=5,
            end_col=5,
            width=65
        )
    )

    requests.append(
        client.update_font_request(
            sheet_id=ws_id,
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        client.center_sheet_request(sheet_id=ws_id)
    )

    requests.append(
        client.format_date_column_request(
            sheet_id=ws_id,
            column=1
        )
    )

    requests.append(
        client.update_range_color_request(
            sheet_id=ws_id,
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            color=(224.95,224.95,224.95)
        )
    )
    print(GREEN + 'Done\n' + RESET)

    print('[Contests] sending style queries...\t')
    client.send_batch_request(ws, requests)
    print()
    ws.update(
        range_name="A1:E1",
        values=[["Date", "Contest Name", "Weight", "Short Name", "URL"]]
    )
