"""Lambda function to fetch financial data and save to Google Sheet."""

# Import from standard library
import os

# Import from other modules
from modules.sheet import GoogleSheet
from modules.finance import Yahoo

# Define global variables
SYMBOL = os.environ.get("SYMBOL")


def lambda_handler(event: dict = {}, context: dict = {}) -> None:
    """Invoke lambda function.

    Args:
        event: Lambda event
        context: Lambda context (unused)
    """
    data = Yahoo(SYMBOL, ["date", "close", "volume"]).history()
    GoogleSheet().update(data.to_dict("records"), "data")
