import json
import src.google_sheets.client as client
import src.google_sheets.services as srv
import src.google_sheets.styler as S


def check_sheets(sheet):
    required_worksheets = ['Participants','Contests','Main']
    existing_worksheets = {ws.title for ws in sheet.worksheets()}
    return all(ws in existing_worksheets for ws in required_worksheets)





if __name__ == '__main__':
    
    with open("config.json", "r") as f:
        config = json.load(f)

    gc = client.GoogleClient("key.json")

    sheet = gc.open_sheet(config["sheet_url"])

    # Select a worksheet/tab
    # worksheet = sheet.worksheet("Test")
    id_sheet = sheet.worksheet("Participants")

    from src.platforms import codeforces as cf

    ids = set()
    cf_ifs = id_sheet.col_values(2)[1:7]
    names = id_sheet.col_values(1)[1:7]

    n_i_dict = {
        id: name 
        for id, name in zip(cf_ifs, names)
    }

    for v in cf_ifs:
        ids.add(v)


    print('participants:')
    print(n_i_dict)

    print("reciving contest standings from cf...")
    data = cf.adapter.get_contest_results(ids,2131)
    print("data received")

    print([p.username for p in data.participants])
    
    print("recording in sheet...")
    srv.create_contest_standings_page(sheet,data,n_i_dict,"CF_1042",50)
    print("Done !")    

