from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union
import gspread


class GoogleSpreadSheet:
    def __init__(self, spreadSheet: gspread.Spreadsheet) -> None:
        self._sheet: gspread.Spreadsheet = spreadSheet

    def worksheet(self, ws_name: str) -> GoogleWorksheet:
        ws: gspread.Worksheet = self._sheet.worksheet(ws_name)
        return GoogleWorksheet(self, ws)

    def worksheets(self) -> List[GoogleWorksheet]:
        return [
            GoogleWorksheet(self, ws)
            for ws in self._sheet.worksheets()
        ]

    def send_batch_request(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._sheet.batch_update({
            "requests": requests
        })

    def del_worksheet(self, worksheet: gspread.Worksheet) -> None:
        self._sheet.del_worksheet(worksheet)

    def add_worksheet(self, name: str, rows: int, columns: int) -> GoogleWorksheet:
        ws: gspread.Worksheet = self._sheet.add_worksheet(name, rows, columns)
        return GoogleWorksheet(self, ws)


class GoogleWorksheet:
    def __init__(self, parent: GoogleSpreadSheet, worksheet: gspread.Worksheet) -> None:
        self._ws: gspread.Worksheet = worksheet
        self.parent: GoogleSpreadSheet = parent

    @property
    def title(self) -> str:
        return self._ws.title

    @property
    def id(self) -> int:
        return self._ws.id

    def col_values(self, col: int) -> list[Any]:
        return self._ws.col_values(col)

    def update(
        self,
        values: List[List[Any]],
        range_name: Optional[str] = None,
        row: Optional[int] = None,
        col: Optional[int] = None,
        value_input_option: str = "RAW",
    ) -> Dict[str, Any]:

        if range_name is None:
            if row is None or col is None:
                raise ValueError(
                    "Either range_name or both row and col must be provided."
                )
            range_name = gspread.utils.rowcol_to_a1(row, col)

        return self._ws.update(
            range_name=range_name,
            values=values,
            value_input_option=value_input_option,
        )


    def clear_worksheet_request(self) -> Dict[str, Any]:
        return {
            "updateCells": {
                "range": {
                    "sheetId": self._ws.id
                },
                "fields": "*"
            }
        }

    def update_row_height_request(
        self,
        *,
        start_row: int,
        end_row: int,
        height: int
    ) -> Dict[str, Any]:
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

    def update_column_width_request(
        self,
        *,
        start_col: int,
        end_col: int,
        width: int
    ) -> Dict[str, Any]:
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

    def update_range_color_request(
        self,
        *,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        color: Union[Tuple[int, int, int], List[int]]
    ) -> Dict[str, Any]:
        normalized_color = (
            color[0] / 255.0,
            color[1] / 255.0,
            color[2] / 255.0
        )

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
                            "red": normalized_color[0],
                            "green": normalized_color[1],
                            "blue": normalized_color[2]
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }

    def update_font_request(
        self,
        *,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        horizontalAlignment: Optional[str] = None,
        verticalAlignment: Optional[str] = None,
        color: Optional[Union[Tuple[int, int, int], List[int]]] = None,
        **text_format: Any
    ) -> Dict[str, Any]:
        if color is not None:
            text_format["foregroundColor"] = {
                "red": color[0] / 255.0,
                "green": color[1] / 255.0,
                "blue": color[2] / 255.0
            }

        user_entered_format: Dict[str, Any] = {
            "textFormat": text_format
        }

        fields_list: List[str] = [f"userEnteredFormat.textFormat.{k}" for k in text_format]

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

    def update_formula_request(
        self,
        *,
        start_row: int,
        end_row: int,
        column: int,
        formula: str
    ) -> Dict[str, Any]:
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

    def center_sheet_request(self) -> Dict[str, Any]:
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

    def format_date_column_request(
        self,
        *,
        column: int,
        pattern: str = "yyyy-mm-dd"
    ) -> Dict[str, Any]:
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

    def update_frozen_request(
        self,
        *,
        frozen_rows: Optional[int] = None,
        frozen_columns: Optional[int] = None
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {"sheetId": self._ws.id}
        fields: List[str] = []

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

    def send_batch_request(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.parent.send_batch_request(requests)