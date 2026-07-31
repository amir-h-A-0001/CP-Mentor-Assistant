import gspread

def clear_worksheet_request(*, sheet_id):
    return {
        "updateCells": {
            "range": {
                "sheetId": sheet_id
            },
            "fields": "*"
        }
    }


def update_row_height_request(*, sheet_id, start_row, end_row, height):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start_row - 1,
                "endIndex": end_row
            },
            "properties": {
                "pixelSize": height
            },
            "fields": "pixelSize"
        }
    }


def update_column_width_request(*, sheet_id, start_col, end_col, width):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": start_col - 1,
                "endIndex": end_col
            },
            "properties": {
                "pixelSize": width
            },
            "fields": "pixelSize"
        }
    }


def update_range_color_request(*, sheet_id, start_row, end_row, start_col, end_col, color):
    color=(color[0]/255, color[1]/255, color[2]/255)

    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row - 1,
                "endRowIndex": end_row,
                "startColumnIndex": start_col - 1,
                "endColumnIndex": end_col
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                }
            },
            "fields": "userEnteredFormat.backgroundColor"
        }
    }


def update_font_request(
    *,
    sheet_id,
    start_row,
    end_row,
    start_col,
    end_col,
    horizontalAlignment=None,
    verticalAlignment=None,
    color=None,
    **text_format
):
    if color is not None:
        text_format["foregroundColor"] = {
            "red": color[0] / 255.0,
            "green": color[1] / 255.0,
            "blue": color[2] / 255.0
        }

    user_entered_format = {
        "textFormat": text_format
    }

    fields_list = [f"userEnteredFormat.textFormat.{k}" for k in text_format]

    if horizontalAlignment is not None:
        user_entered_format["horizontalAlignment"] = horizontalAlignment
        fields_list.append("userEnteredFormat.horizontalAlignment")

    if verticalAlignment is not None:
        user_entered_format["verticalAlignment"] = verticalAlignment
        fields_list.append("userEnteredFormat.verticalAlignment")

    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row - 1,
                "endRowIndex": end_row,
                "startColumnIndex": start_col - 1,
                "endColumnIndex": end_col
            },
            "cell": {
                "userEnteredFormat": user_entered_format
            },
            "fields": ",".join(fields_list)
        }
    }


def update_formula_request(*, sheet_id, start_row, end_row, column, formula):
    
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row - 1,
                "endRowIndex": end_row,
                "startColumnIndex": column - 1,
                "endColumnIndex": column
            },
            "cell": {
                "userEnteredValue": {
                    "formulaValue": formula
                }
            },
            "fields": "userEnteredValue"
        }
    }

def center_sheet_request(*, sheet_id):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": (
                "userEnteredFormat.horizontalAlignment,"
                "userEnteredFormat.verticalAlignment"
            )
        }
    }


def format_date_column_request(*, sheet_id, column, pattern="yyyy-mm-dd"):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startColumnIndex": column - 1,
                "endColumnIndex": column
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "DATE",
                        "pattern": pattern
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }


def update_frozen_request(*, sheet_id, frozen_rows=None, frozen_columns=None):
    properties = {"sheetId": sheet_id}
    fields = []

    if frozen_rows is not None:
        properties["gridProperties"] = properties.get("gridProperties", {})
        properties["gridProperties"]["frozenRowCount"] = frozen_rows
        fields.append("gridProperties.frozenRowCount")

    if frozen_columns is not None:
        properties["gridProperties"] = properties.get("gridProperties", {})
        properties["gridProperties"]["frozenColumnCount"] = frozen_columns
        fields.append("gridProperties.frozenColumnCount")

    return {
        "updateSheetProperties": {
            "properties": properties,
            "fields": ",".join(fields)
        }
    }



def send_batch_request(worksheet, requests):
    RESET = "\033[0m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    try:
        result = worksheet.spreadsheet.batch_update({
            "requests": requests
        })
        print(GREEN + "Success\n" + RESET)
        return result
    except Exception as e:
        print(RED + "Failed:", e, RESET)
        return None
