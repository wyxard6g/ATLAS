from atlas.backtesting.window import SlidingWindowBuilder
from atlas.domain.candle import Candle
from atlas.domain.feature_set import FeatureSet
from atlas.features.engine import FeatureEngine


class BacktestFeaturePipeline:
    """
    Builds MarketData windows and computes FeatureSets during backtests.
    """

    def __init__(
        self,
        candles: list[Candle],
        symbol: str,
        timeframe: str,
        feature_engine: FeatureEngine,
    ):
        self._window_builder = SlidingWindowBuilder(
            candles=candles,
            symbol=symbol,
            timeframe=timeframe,
        )
        self._feature_engine = feature_engine

    def compute_at(self, end_index: int) -> FeatureSet:
        market_data = self._window_builder.build(end_index=end_index)

        return self._feature_engine.compute(market_data)