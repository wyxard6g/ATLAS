from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class RelativeStrengthIndex(Feature):
    """
    Relative Strength Index (RSI).
    """

    def __init__(self, period: int = 14):
        if period <= 0:
            raise ValueError("Period must be greater than 0.")

        self.period = period

    @property
    def name(self) -> str:
        return f"rsi_{self.period}"

    def compute(self, context: FeatureContext) -> float:
        closes = context.closes

        if len(closes) <= self.period:
            raise ValueError("Not enough candles to compute RSI.")

        gains = []
        losses = []

        for i in range(1, len(closes)):
            change = closes[i] - closes[i - 1]
            gains.append(max(change, 0))
            losses.append(abs(min(change, 0)))

        avg_gain = sum(gains[-self.period:]) / self.period
        avg_loss = sum(losses[-self.period:]) / self.period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))