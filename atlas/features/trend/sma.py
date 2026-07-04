from atlas.features.base import Feature
from atlas.features.context import FeatureContext


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

    def compute(self, context: FeatureContext) -> float:
        if context.count < self.period:
            raise ValueError("Not enough candles to compute SMA.")

        return sum(context.closes[-self.period:]) / self.period