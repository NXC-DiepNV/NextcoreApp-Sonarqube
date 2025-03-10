from typing import List

from google.oauth2.service_account import Credentials
import gspread
from gspread import Worksheet, Spreadsheet


class SheetCore:
    scope_default = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    ROW_DEFAULT = 100
    COLUMN_DEFAULT = 100

    def __init__(self, account_file: str, scopes: List[str] = None, spreadsheet_id: str = None, sheet_title: str = None) -> None:
        scopes = self.scope_default if scopes is None else scopes
        credentials = Credentials.from_service_account_file(
            account_file,
            scopes=scopes
        )

        self.client = gspread.authorize(credentials)

        if spreadsheet_id:
            self.spreadsheet = self.open_spreadsheet_by_key(spreadsheet_id)

            if sheet_title:
                self.worksheet = self.spreadsheet.worksheet(sheet_title)

    def open_spreadsheet_by_key(self, spreadsheet_id: str) -> Spreadsheet:
        return self.client.open_by_key(spreadsheet_id)

    def open_sheet_by_title(self, sheet_title: str) -> Worksheet:
        self.worksheet = self.spreadsheet.worksheet(sheet_title)
        return self.worksheet

    def create_new_sheet(self, sheet_title: str) -> Worksheet:
        self.worksheet = self.spreadsheet.add_worksheet(
            title=sheet_title,
            rows=self.ROW_DEFAULT,
            cols=self.COLUMN_DEFAULT
        )
        return self.worksheet
