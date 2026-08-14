import json
import gspread
from . import spreadsheet 


def prepare_participants_ws(worksheet):

    requests = []

    requests.append(
        worksheet.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
    ))

    requests.append(
        worksheet.update_column_width_request(
            start_col=1,
            end_col=1,
            width=214
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=2,
            end_col=3,
            width=130
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        worksheet.center_sheet_request()
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=3,
            color=(239,239,239)
        )
    )

    worksheet.send_batch_request(requests)


def prepare_contests_list_ws(worksheet):

    requests = []

    requests.append(
        worksheet.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
    ))

    requests.append(
        worksheet.update_column_width_request(
            start_col=1,
            end_col=1,
            width=144
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=2,
            end_col=2,
            width=340
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=3,
            end_col=3,
            width=70
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=4,
            end_col=4,
            width=130
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=5,
            end_col=5,
            width=65
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            fontFamily="Lexend",
            fontSize=12
        )
    )

    requests.append(
        worksheet.center_sheet_request()
    )

    requests.append(
        worksheet.format_date_column_request(
            column=1
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=5,
            color=(239,239,239)
        )
    )

    worksheet.send_batch_request(requests)


def prepare_contest_standings_ws(worksheet, short_name, indices):

    problems_count = len(indices)
    requests = []

    requests.append(
        worksheet.center_sheet_request()
        )

    requests.append(
        worksheet.update_row_height_request(
            start_row=1,
            end_row=1,
            height=42
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=1,
            end_col=1,
            width=52
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=2,
            end_col=2,
            width=214
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=3,
            end_col=3,
            width=55
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=4,
            end_col=4,
            width=60
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=5,
            end_col=5,
            width=5
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=6,
            end_col=6-1 + problems_count,
            width=62
        )
    )

    split = 6 + problems_count
    requests.append(
        worksheet.update_column_width_request(
            start_col=split,
            end_col=split,
            width=5
        )
    )

    requests.append(
        worksheet.update_column_width_request(
            start_col=split+1,
            end_col=split+1,
            width=100
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=split+1,
            color=(239, 239, 239)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=5,
            end_col=5,
            color=(153,153,153)
        )
    )

    requests.append(
        worksheet.update_frozen_request(
            frozen_rows=1,
            frozen_columns=2
        )
    )

    requests.append(
        worksheet.update_row_height_request(
            start_row=2,
            end_row=2,
            height=8
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=split+1,
            fontFamily="Lexend"
        )
    )

    worksheet.send_batch_request(requests)


def _accepted_cell_style(worksheet, row, col):
    requests = []

    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=col,
            end_col=col,
            color=(217,234,211)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=row,
            end_row=row,
            start_col=col,
            end_col=col,
            bold= True,
            color=(56,118,29)
        )
    )

    return requests

def _rejected_cell_style(worksheet, row, col):
    requests = []

    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=col,
            end_col=col,
            color=(244,204,204)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=row,
            end_row=row,
            start_col=col,
            end_col=col,
            bold=True,
            color=(204,0,0)
        )
    )

    return requests

def prepare_contest_standing_row(worksheet, row, judge_results):

    problems_count = len(judge_results)
    requests = []

    requests.append(
        worksheet.update_row_height_request(
            start_row=row,
            end_row=row,
            height=36
        )
    )

    requests.append(
        worksheet.update_row_height_request(
            start_row=row+1,
            end_row=row+1,
            height=23
        )
    )

    requests.append(
        worksheet.update_row_height_request(
            start_row=row+2,
            end_row=row+2,
            height=8
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=1,
            end_col=2,
            color=(204,204,204)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=3,
            end_col=4,
            color=(217,217,217)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=row,
            end_row=row+1,
            start_col=1,
            end_col=4,
            fontFamily="Lexend"
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=row+1,
            end_row=row+1,
            start_col=1,
            end_col=4,
            color=(102,102,102)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=5,
            end_col=5,
            color=(153,153,153)
        )
    )


    start_col = 6
    requests.append(
        worksheet.update_range_color_request(
            start_row=row,
            end_row=row+1,
            start_col=start_col,
            end_col=start_col + problems_count + 1,
            color=(239,239,239)
        )
    )

    requests.append(
        worksheet.update_font_request(
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
        requests.extend(cell_style(worksheet, row,start_col+i))

    worksheet.send_batch_request(requests)


def _results_header(worksheet,length):

    requests = []

    requests.append(
        worksheet.merge_cells_request(
            start_row=1,
            end_row=1,
            start_col=2,
            end_col=length - 1,
        )
    )

    requests.append(
        worksheet.update_row_height_request(
            start_row=1,
            end_row=1,
            height=150
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=length,
            color=(255,242,204)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=1,
            end_row=1,
            start_col=1,
            end_col=length,
            font_family="Oswald",
            font_size=24,
            bold=True,
            color=(180, 95, 6)
        )
    )

    return requests

def _result_column(worksheet, rows, header_row, column_idx):

    requests = []

    requests.append(
        worksheet.merge_cells_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx,
            end_col=column_idx+1
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx,
            end_col=column_idx,
            color=(247,203,77)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row+2,
            end_row= header_row+2 + rows - 1,
            start_col=column_idx,
            end_col= column_idx + 1,
            color= (255,229,153) if (column_idx // 2) % 2 == 0 else (255,242,204)
        )
    )

    return requests


def _names_culumn(worksheet, rows, header_row, column_idx):

    requests = []

    requests.append(
        worksheet.update_column_width_request(
            start_col=column_idx,
            end_col=column_idx,
            width=150
        )
    )

    requests.append(
            worksheet.merge_cells_request(
                start_row=header_row,
                end_row=header_row+1,
                start_col=column_idx,
                end_col=column_idx
            )
        )

    requests.append(
        worksheet.update_row_height_request(
            start_row=header_row+2,
            end_row= header_row+2 + rows -1,
            height=42 
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row,
            end_row=header_row+1,
            start_col=column_idx,
            end_col=column_idx,
            color=(38,166,154)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row+2,
            end_row= header_row+2 + rows - 1,
            start_col=column_idx,
            end_col=column_idx,
            color=(221,242,240)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=header_row+2,
            end_row=header_row+2 + rows - 1,
            start_col=column_idx,
            end_col=column_idx,
            font_family="Georgia"
        )
    )

    return requests

def _absence_column(worksheet, rows, header_row, column_idx):

    requests = []

    requests.append(
        worksheet.update_column_width_request(
            start_col=column_idx,
            end_col=column_idx,
            width=150
        )
    )

    requests.append(
        worksheet.merge_cells_request(
            start_row=header_row,
            end_row=header_row+1,
            start_col=column_idx,
            end_col=column_idx
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx,
            end_col=column_idx,
            color=(204,65,37)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row+2,
            end_row=header_row+2 + rows - 1,
            start_col=column_idx,
            end_col=column_idx,
            color=(221,126,107)
        )
    )
    
    return requests



def _final_scores_columns(worksheet, rows, header_row, column_idx):

    requests = []

    requests.append(
        worksheet.update_column_width_request(
            start_col=column_idx+1,
            end_col=column_idx+1,
            width=150
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx,
            end_col=column_idx,
            color=(241,194,50)
        )
    )
    
    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row+2,
            end_row= header_row+2 + rows - 1,
            start_col=column_idx,
            end_col= column_idx,
            color= (255,229,153) if (column_idx // 2) % 2 == 0 else (255,242,204)
        )
    )

    requests.append(
        worksheet.update_font_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx,
            end_col=column_idx + 1,
            color=(255,255,255)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row,
            end_row=header_row,
            start_col=column_idx + 1,
            end_col=column_idx + 1,
            color=(204,65,37)
        )
    )

    requests.append(
        worksheet.update_range_color_request(
            start_row=header_row+2,
            end_row=header_row+2 + rows - 1,
            start_col=column_idx + 1,
            end_col=column_idx + 1,
            color=(221,126,107)
        )
    )

    return requests


def prepare_results_page(worksheet, rows, columns, final):

    header_row = 1
    requests = []

    requests.append(
        worksheet.center_sheet_request()
    )

    if final:
        requests.extend(
            _results_header(
                worksheet=worksheet,
                length=columns * 2 + (3 if final else 2)
            )
        )
        header_row = 2

    requests.append(
        worksheet.update_font_request(
            start_row=header_row,
            end_row= header_row + 2 + rows - 1,
            start_col=1,
            end_col= columns * 2 + (3 if final else 2),
            font_family="Oswald"
        )
    )

    requests.extend(
        _names_culumn(
            worksheet,
            header_row=header_row,
            column_idx=1,
            rows=rows
        )
    )

    for i in range(columns):
        requests.extend(
            _result_column(
                worksheet=worksheet,
                rows=rows,
                header_row=header_row,
                column_idx= 2 + i * 2
            )
        )

    last_columns = _final_scores_columns if final else _absence_column

    requests.extend(
        last_columns(
            worksheet=worksheet,
            rows=rows,
            header_row=header_row,
            column_idx= 2 + columns * 2
        )
    )

    requests.append(
        worksheet.update_frozen_request(
            frozen_rows= 3 if final else 2,
            frozen_columns=1
        )
    )

    worksheet.send_batch_request(requests)