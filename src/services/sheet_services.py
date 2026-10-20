from src.google_sheets import services, reader

def create_All_ws(sheet):

    participants = reader.get_participant_names(sheet)

    data = {
        'contests':[],
        'results':{
            name:[]
            for name in participants
        }
    }

    services.create_all_results_page(sheet, data)