import json
import src.google_sheets.client as client
import src.google_sheets.services as srv
import src.google_sheets.reader as rdr
import src.services.contest_service as csrv

if __name__ == '__main__':
    
    with open("config.json", "r") as f:
        config = json.load(f)

    gc = client.GoogleClient("key.json")

    sheet = gc.open_sheet(config["sheet_url"])

    # ws = sheet.worksheet('Contests')
    # print(ws.row_values(2))
    # print(ws.row_values(3))
    # print(ws.row_values(4))

    
    # print(rdr.get_all_contests(sheet))

    csrv.add_batch_contests(sheet,False,False)



    # id_sheet = sheet.worksheet("Participants")
    # names = id_sheet.col_values(1)[1:7]
    # srv.create_all_results_page(sheet,names,10,20)

    # data = {
    #     'contests':["c1","c2","c3"],
    #     'results': {
    #         'participant_1': [[1000,1],[2000,2],[3000,3]],
    #         'participant_2': [[1000,3],[],[3000,3]],
    #         'participant_3': [[1000,4],[2000,2],[]],
    #         'participant_4': [[1000,5],[2000,2],[3500,4]],
    #     }
    # }

    # srv.create_final_results_page(sheet,"semiFinal",4,3,data)

    # names = rdr.get_participant_names(sheet)

    # data = {
    #     'contests':[],
    #     'results':{
    #         name:[] 
    #         for name in names
    #     }
    # }

    # srv.create_all_results_page(sheet, data)

    # import src.services.contest_service as csrv

    # csrv.add_contest(sheet,"cf 1042","https://codeforces.com/contest/2131",False)


    # data = [[1000,1],[2000,6],[],[1500,2]]
    # srv.add_contest_to_all(sheet,"test",data)



    # from src.google_sheets import writer

    # ws = sheet.worksheet("t2")
    # data = {
    #     'contests':["c1","c2","c3"],
    #     'results': {
    #         'participant_1': [[1000,1],[2000,2],[3000,3]],
    #         'participant_2': [[1000,1],[],[3000,3]],
    #         'participant_3': [[1000,1],[2000,2],[]],
    #         'participant_4': [[1000,1],[2000,2],[3500,4]],
    #     }
    # }
    # writer.write_results(ws,data,False)




    # Select a worksheet/tab
    # worksheet = sheet.worksheet("t2")

    # S.prepare_results_page(worksheet,12,10,final=False)


    # s = sheet.index_to_a1(4,2)
    # e = sheet.index_to_a1(4,21)

    # print(s,e)
    # print(f"=COUNTBLANK({s}:{e}) / 2")

    # worksheet.send_batch_request(
    #     worksheet.update_formula_request(
    #         start_row=4,
    #         end_row=12,
    #         column=22,
    #         formula=f"=COUNTBLANK({s}:{e}) / 2"
    #     )
    # )

    # id_sheet = sheet.worksheet("Participants")

    # from src.platforms import codeforces as cf

    # ids = set()
    # cf_ifs = id_sheet.col_values(2)[1:7]
    # names = id_sheet.col_values(1)[1:7]

    # n_i_dict = {
    #     id: name 
    #     for id, name in zip(cf_ifs, names)
    # }

    # for v in cf_ifs:
    #     ids.add(v)


    # print('participants:')
    # print(n_i_dict)

    # print("reciving contest standings from cf...")
    # data = cf.adapter.get_contest_results(ids,2257)
    # print("data received")

    # print([p.username for p in data.participants])
    
    # print("recording in sheet...")
    # srv.create_contest_standings_page(sheet,data,n_i_dict,"CF_new",50)
    # print("Done !")    

