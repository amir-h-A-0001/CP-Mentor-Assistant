import gspread
from .spreadsheet import GoogleSpreadSheet

class GoogleClient:
    def __init__(self, creds_path: str):
            self._gc = gspread.service_account(filename=creds_path)

    def open_sheet(self, url: str) -> GoogleSpreadSheet:
        return GoogleSpreadSheet(self._gc.open_by_url(url))

    def share_spreadsheet(self, spreadsheet_url_or_key: str, email: str, role: str = "reader", notify: bool = True):
        """Shares a Google Spreadsheet with a user.

        :param spreadsheet_url_or_key: URL or File ID of the spreadsheet.
        :param email: Email address of the person/account to share with.
        :param role: 'writer' (editor), 'reader' (viewer), or 'commenter'. Defaults to 'reader'.
        :param notify: Whether to send an email notification from Google. Defaults to True.
        """
        if spreadsheet_url_or_key.startswith("https://"):
            sheet = self._gc.open_by_url(spreadsheet_url_or_key)
        else:
            sheet = self._gc.open_by_key(spreadsheet_url_or_key)

        sheet.share(
            email_address=email,
            perm_type="user",
            role=role,
            notify=notify
        )