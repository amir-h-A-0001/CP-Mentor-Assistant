import json
import gspread
import src.google_sheets.styler as S


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
    id_sheet = sheet.worksheet("Participants")



    # S.create_contest_ws(sheet,"C1",['A','B','C','C2','D','E'])
    S.prepare_contest_standing_row(sheet.worksheet("C1"),3,[1,1,-1,0,-1,0])


    # from src.platforms import codeforces as cf

    # ids = set()
    # values = id_sheet.col_values(2)[1:6]

    # for v in values:
    #     ids.add(v)

    # data = cf.adapter.get_contest_results(ids,2131)
    # print(data)
    

