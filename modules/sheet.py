"""Save data to Google Sheet."""

# Import from standard library
from typing import List, Dict

# Import from 3rd party libraries
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials


class GoogleSheet:
    """Google Sheet connector."""

    credentials = Credentials.from_service_account_file(
        "google_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    sheets_service = build(
        "sheets", "v4", credentials=credentials, cache_discovery=False
    )
    sheet_id = "1ckprgk_Y-rA0Kw7OxC_rq8T2yK6UQMQoJ58GkkAuyV0"

    def update(self, data: List[Dict], tab_name: str) -> None:
        """Update data in Google Sheet.

        Args:
            data: List of dictionaries with (CSV) data to be saved.
            tab_name: Name of the tab in the Google Sheet.
        """
        # Add sheet (tab) to spreadsheet if it does not exist
        try:
            result = (
                self.sheets_service.spreadsheets()
                .batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={
                        "requests": [{"addSheet": {"properties": {"title": tab_name}}}]
                    },
                )
                .execute()
            )
        except HttpError:
            pass

        # Update values
        header = [key for key, val in data[0].items()]
        rows = [[val for key, val in row.items()] for row in data]
        rows.insert(0, header)

        result = (
            self.sheets_service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.sheet_id,
                range=f"{tab_name}!A1:AZ",
                valueInputOption="USER_ENTERED",
                body={"values": rows},
            )
            .execute()
        )

        print(f"{result.get('updatedCells')} cells updated")
