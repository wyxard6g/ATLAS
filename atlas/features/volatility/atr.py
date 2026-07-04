from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class AverageTrueRange(Feature):
    """
    Average True Range volatility feature.
    """

    def __init__(self, period: int = 14):
        if period <= 0:
            raise ValueError("Period must be greater than 0.")

        self.period = period

    @property
    def name(self) -> str:
        return f"atr_{self.period}"

    def compute(self, context: FeatureContext) -> float:
        if context.count <= self.period:
            raise ValueError("Not enough candles to compute ATR.")

        true_ranges = []

        for i in range(1, context.count):
            high = context.highs[i]
            low = context.lows[i]
            previous_close = context.closes[i - 1]

            true_range = max(
                high - low,
                abs(high - previous_close),
                abs(low - previous_close),
            )

            true_ranges.append(true_range)

        return sum(true_ranges[-self.period:]) / self.period