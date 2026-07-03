from atlas.domain.market_data import MarketData
from atlas.features.base import Feature


class SimpleMovingAverage(Feature):
    """
    Simple Moving Average feature.
    """

    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("Period must be greater than 0.")

        self.period = period

    @property
    def name(self) -> str:
        return f"sma_{self.period}"

    def compute(self, market_data: MarketData) -> float:
        if market_data.count < self.period:
            raise ValueError("Not enough candles to compute SMA.")

        closes = [candle.close for candle in market_data.candles]

        return sum(closes[-self.period:]) / self.period