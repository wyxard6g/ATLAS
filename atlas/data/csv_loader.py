import csv
from datetime import datetime

from atlas.domain.candle import Candle


class CSVLoader:
    """
    Loads OHLCV candle data from a CSV file.
    """

    def load(self, path: str) -> list[Candle]:
        candles = []

        with open(path, newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                candles.append(
                    Candle(
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                    )
                )

        return candles