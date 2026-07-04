from atlas.features.base import Feature
from atlas.features.context import FeatureContext


class OnBalanceVolume(Feature):
    """
    On-Balance Volume feature.
    """

    @property
    def name(self) -> str:
        return "obv"

    def compute(self, context: FeatureContext) -> float:
        if context.count < 2:
            raise ValueError("Not enough candles to compute OBV.")

        obv = 0.0

        for i in range(1, context.count):
            if context.closes[i] > context.closes[i - 1]:
                obv += context.volumes[i]
            elif context.closes[i] < context.closes[i - 1]:
                obv -= context.volumes[i]

        return obv