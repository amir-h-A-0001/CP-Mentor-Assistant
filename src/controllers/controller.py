
from src.google_sheets import client
from src.services import config_services, contest_services, report_services, participant_services


class Controller:
    def __init__(self):
        self.gc = client.GoogleClient(config_services.get_creds_path())
        self._sheet_name = None
        self._sheet = None

        self.switch_sheet("main")

    @property
    def sheet_name(self) -> str:
        return self._sheet_name

    def switch_sheet(self, name: str) -> None:
        """Switch the active spreadsheet."""
        url = config_services.get_sheet_url(name)
        self._sheet = self.gc.open_sheet(url)
        self._sheet_name = name

    def get_sheet_names(self) -> list[str]:
        return config_services.get_sheet_names()

    def add_contest(
        self,
        short_title: str,
        url: str,
        include_virtuals: bool,
        create_standings: bool,
        exists: bool = False,
        platform_name: str | None = None,
        weight: float | None = None,
    ):

        participant_services.add_new_participants(self._sheet)
        
        return contest_services.add_contest(
            self._sheet,
            short_title,
            url,
            include_virtuals,
            create_standings,
            exists=exists,
            platform_name=platform_name,
            weight=weight,
        )

    def add_batch_contests(
        self,
        include_virtuals: bool,
        create_standings: bool,
    ):
        
        participant_services.add_new_participants(self._sheet)
        
        return contest_services.add_batch_contests(
            self._sheet,
            include_virtuals,
            create_standings,
        )

    def create_final_table(
        self,
        *,
        title: str,
        number_of_contests: int,
        most_absences,
        best_first: bool,
        weighted: bool,
    ):
        return report_services.create_final_table(
            self._sheet,
            title=title,
            number_of_contests=number_of_contests,
            most_absences=most_absences,
            best_first=best_first,
            weighted=weighted,
        )
