import gspread

class GoogleSpreadSheet:
    def __init__(self, spreadSheet):
        self._sheet = spreadSheet        

    def worksheet(self, ws_name):
        ws = self._sheet.worksheet(ws_name)
        return GoogleWorksheet(self, ws)

    def worksheets(self):
        return [
            GoogleWorksheet(self, ws)
            for ws in self._sheet.worksheets()
        ]

    def send_batch_request(self, requests):
        return self._sheet.batch_update({
            "requests": requests
        })

    def del_worksheet(self, worksheet):
        self._sheet.del_worksheet(worksheet)

    def add_worksheet(self, name, rows, columns):
        ws = self._sheet.add_worksheet(name, rows, columns)
        return GoogleWorksheet(self, ws)



class GoogleWorksheet:
    def __init__(self, parent, worksheet):
        self._ws = worksheet
        self.parent = parent

    @property
    def title(self):
        return self._ws.title

    @property
    def id(self):
        return self._ws.id

    def update(
        self,
        range_name: str,
        values,
        value_input_option="RAW"
    ):
        self._ws.update(
            range_name=range_name,
            values=values,
            value_input_option=value_input_option,
        )


    def clear_worksheet_request(*, sheet_id):
        return {
            "updateCells": {
                "range": {
                    "sheetId": sheet_id
                },
                "fields": "*"
            }
        }


    def update_row_height_request(self, *, start_row, end_row, height):
        return {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": self._ws.id,
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


    def update_column_width_request(self, *, start_col, end_col, width):
        return {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": self._ws.id,
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


    def update_range_color_request(self, *, start_row, end_row, start_col, end_col, color):
        color=(color[0]/255, color[1]/255, color[2]/255)

        return {
            "repeatCell": {
                "range": {
                    "sheetId": self._ws.id,
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
        self, *,
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
                    "sheetId": self._ws.id,
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


    def update_formula_request(self, *, start_row, end_row, column, formula):
        
        return {
            "repeatCell": {
                "range": {
                    "sheetId": self._ws.id,
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

    def center_sheet_request(self):
        return {
            "repeatCell": {
                "range": {
                    "sheetId": self._ws.id
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


    def format_date_column_request(self, *, column, pattern="yyyy-mm-dd"):
        return {
            "repeatCell": {
                "range": {
                    "sheetId": self._ws.id,
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


    def update_frozen_request(self, *,frozen_rows=None, frozen_columns=None):
        properties = {"sheetId": self._ws.id}
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

    def send_batch_request(self, requests):
        return self.parent.send_batch_request(requests)
    
