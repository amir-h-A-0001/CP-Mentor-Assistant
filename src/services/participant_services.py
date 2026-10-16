from src.google_sheets import services, reader

def add_new_participants(sheet):

    names = reader.get_participant_names(sheet)
    recorded_names = reader.get_recorded_participants(sheet)

    needed_rows = names[len(recorded_names):]

    if len(needed_rows) == 0:
        return

    services.append_rows_to_all(sheet, needed_rows)