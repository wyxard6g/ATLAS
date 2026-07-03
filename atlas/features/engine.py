from atlas.domain.market_data import MarketData
from atlas.features.registry import FeatureRegistry


class FeatureEngine:
    """
    Computes every registered feature.
    """

    def __init__(self, registry: FeatureRegistry):
        self._registry = registry

    def compute(self, market_data: MarketData) -> dict:
        results = {}

        for feature in self._registry.all():
            results[feature.name] = feature.compute(market_data)

        return results