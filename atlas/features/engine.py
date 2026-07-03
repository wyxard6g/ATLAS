from atlas.domain.feature_set import FeatureSet
from atlas.domain.market_data import MarketData
from atlas.features.registry import FeatureRegistry


class FeatureEngine:
    """
    Computes every registered feature and returns a FeatureSet.
    """

    def __init__(self, registry: FeatureRegistry):
        self._registry = registry

    def compute(self, market_data: MarketData) -> FeatureSet:
        results = {}

        for feature in self._registry.all():
            results[feature.name] = feature.compute(market_data)

        return FeatureSet(
            symbol=market_data.symbol,
            timeframe=market_data.timeframe,
            timestamp=market_data.end_time,
            features=results,
        )