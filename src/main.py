import json
import gspread
import styler as S


def check_sheets(sheet):
    required_worksheets = ['Participants','Contests','Main']
    existing_worksheets = {ws.title for ws in sheet.worksheets()}
    return all(ws in existing_worksheets for ws in required_worksheets)








if __name__ == '__main__':
    
    with open("config.json", "r") as f:
        config = json.load(f)

    gc = gspread.service_account(filename="key.json")

    sheet = gc.open_by_url(config["sheet_url"])



    # Select a worksheet/tab
    worksheet = sheet.worksheet("Test")
