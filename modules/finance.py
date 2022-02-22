"""Load data from Yahoo Finance."""

# Import from 3rd party libraries
import pandas as pd
import yahooquery as yq


class Yahoo:
    """Yahoo finance connector."""

    def __init__(self, symbol: str, columns: list):
        self.symbol = symbol
        self.ticker = yq.Ticker([symbol])
        self.columns = columns

    def history(self, period: str = "1y") -> pd.DataFrame:
        history = self.ticker.history(period).reset_index(level=["date"])
        history["date"] = history["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        print(f"Fetched data for {self.symbol}")
        return history[self.columns]
