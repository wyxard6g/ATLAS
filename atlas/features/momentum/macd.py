from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class MACD(Feature):
    """
    Moving Average Convergence Divergence feature.
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ):
        if fast_period <= 0:
            raise ValueError("Fast period must be greater than 0.")

        if slow_period <= 0:
            raise ValueError("Slow period must be greater than 0.")

        if signal_period <= 0:
            raise ValueError("Signal period must be greater than 0.")

        if fast_period >= slow_period:
            raise ValueError("Fast period must be less than slow period.")

        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    @property
    def name(self) -> str:
        return f"macd_{self.fast_period}_{self.slow_period}_{self.signal_period}"

    def compute(self, context: FeatureContext) -> dict[str, float]:
        if context.count < self.slow_period + self.signal_period:
            raise ValueError("Not enough candles to compute MACD.")

        fast_ema = self._ema_series(context.closes, self.fast_period)
        slow_ema = self._ema_series(context.closes, self.slow_period)

        macd_line = [
            fast - slow
            for fast, slow in zip(fast_ema[-len(slow_ema):], slow_ema)
        ]

        signal_line = self._ema_series(macd_line, self.signal_period)

        histogram = macd_line[-1] - signal_line[-1]

        return {
            "macd": macd_line[-1],
            "signal": signal_line[-1],
            "histogram": histogram,
        }

    def _ema_series(self, values: list[float], period: int) -> list[float]:
        multiplier = 2 / (period + 1)

        ema_values = []
        ema = values[0]

        for value in values:
            ema = (value - ema) * multiplier + ema
            ema_values.append(ema)

        return ema_values