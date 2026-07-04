from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class BollingerBands(Feature):
    """
    Bollinger Bands volatility envelope feature.
    """

    def __init__(self, period: int = 20, standard_deviations: float = 2.0):
        if period <= 0:
            raise ValueError("Period must be greater than 0.")

        if standard_deviations <= 0:
            raise ValueError("Standard deviations must be greater than 0.")

        self.period = period
        self.standard_deviations = standard_deviations

    @property
    def name(self) -> str:
        return f"bollinger_bands_{self.period}_{self.standard_deviations}"

    def compute(self, context: FeatureContext) -> dict[str, float]:
        if context.count < self.period:
            raise ValueError("Not enough candles to compute Bollinger Bands.")

        closes = context.closes[-self.period:]

        mean = sum(closes) / self.period
        variance = sum((close - mean) ** 2 for close in closes) / self.period
        standard_deviation = variance ** 0.5

        upper_band = mean + self.standard_deviations * standard_deviation
        lower_band = mean - self.standard_deviations * standard_deviation

        return {
            "middle": mean,
            "upper": upper_band,
            "lower": lower_band,
            "width": upper_band - lower_band,
        }