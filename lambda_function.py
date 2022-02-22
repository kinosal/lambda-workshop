"""Lambda function to fetch financial data and save to Google Sheet."""

# Import from standard library
import os

# Import from other modules
from modules.sheet import GoogleSheet
from modules.finance import Yahoo

# Define global variables
SYMBOL = os.environ.get("SYMBOL")
SHEET_ID = os.environ.get("SHEET_ID")


def lambda_handler(event: dict = {}, context: dict = {}) -> None:
    """Invoke lambda function.

    Args:
        event: Lambda event
        context: Lambda context (unused)
    """
    # Load ticker history form Yahoo
    data = Yahoo(SYMBOL, ["date", "close", "volume"]).history()

    # Save data to Google Sheet
    GoogleSheet(SHEET_ID).update(data.to_dict("records"), "data")
