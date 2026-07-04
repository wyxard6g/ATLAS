from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class ExponentialMovingAverage(Feature):
    """
    Exponential Moving Average feature.
    """

    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("Period must be greater than 0.")

        self.period = period

    @property
    def name(self) -> str:
        return f"ema_{self.period}"

    def compute(self, context: FeatureContext) -> float:
        if context.count < self.period:
            raise ValueError("Not enough candles to compute EMA.")

        closes = context.closes
        multiplier = 2 / (self.period + 1)

        ema = closes[0]

        for close in closes[1:]:
            ema = (close - ema) * multiplier + ema

        return ema