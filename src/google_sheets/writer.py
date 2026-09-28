from . import spreadsheet

def write_participants_list_header(worksheet):
    worksheet.update(
        range_name="A1:C1",
        values=[["FullName", "CF ID", "AtCoder ID"]]
    )


def write_standings_header(worksheet, indices):
    worksheet.update(
            range_name="A1",
            values=[["Rank", "Contestant", "Solved", "Penalty", ""] + indices + ["", "Performance"]]
        )

def write_standings_row(worksheet, participant, username, idx, current_row):
    
        attempts = 0
        for p in participant.problems:
            if p.tried:
                attempts += p.reject_count
            if p.is_solved:
                attempts += 1

        penalty_s = participant.penalty

        hours = penalty_s // 60
        minutes = (penalty_s % 60)

        first_row = (
            [participant.rank, username, participant.solved, penalty_s, '']
            + [
                '' if not p.tried else f"{p.reject_count}{'+' if p.is_solved else '-'}"
                for p in participant.problems
            ]
            + ['', participant.performance]
        )

        second_row = (
            [idx+1, participant.username, attempts, f"{hours}:{minutes:02d}", '']
            + [
                '' if not p.is_solved else (f"{p.accept_time // 3600}:{((p.accept_time % 3600)//60):02d}") for p in participant.problems
            ]
            + ['','']
        )

        worksheet.update(
            row=current_row,
            col=1,
            values=[first_row, second_row],
        )


def write_results_header(worksheet, columns, is_final):
    
    worksheet.update(
        range_name = "A1",
        values=[["Contanstant\\Contest"]]
    )

    pairs = ["Performance","contest_idx"] if is_final else ["Performance","Solve"] 

    worksheet.update(
        range_name = "B2",
        values=[pairs * columns]
    )

def write_absence_column(worksheet, rows, columns):

    absence_col = 1 + columns * 2 + 1
    
    worksheet.update(
        row=1,
        col=absence_col,
        values=[["Absence"]]
    )

    first_start_col = spreadsheet.GoogleSpreadSheet.index_to_a1(3,2)
    first_end_col = spreadsheet.GoogleSpreadSheet.index_to_a1(3, 1 + columns * 2)

    worksheet.send_batch_request(
        worksheet.update_formula_request(
            start_row=3,
            end_row=2 + rows + 5,
            column=absence_col,
            formula=f"=COUNTBLANK({first_start_col}:{first_end_col}) / 2"
        )
    )

def write_results(worksheet, data, has_header):

    # contest names
    c_names = [x for item in data["contests"] for x in (item, '')]

    worksheet.update(
         range_name="B2" if has_header else "B1",
         values= [c_names]
    )

    # participant data
    write_buffer = []

    for name, res in data["results"].items():
        result = [x for contest in res for x in (contest if contest else ['', ''])]
        write_buffer.append([name] + result)

    worksheet.update(
         range_name="A4" if has_header else "A3",
         values=write_buffer
    )

def write_contest_col(worksheet, column, contest_name, results_ordered):

    worksheet.update(
        row= 1,
        col=column,
        values=[[contest_name]]
    )

    worksheet.update(
        row=3,
        col=column,
        values=results_ordered
    )



