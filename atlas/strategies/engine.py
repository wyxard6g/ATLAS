from atlas.domain.feature_set import FeatureSet
from atlas.domain.signal import Signal
from atlas.strategies.registry import StrategyRegistry


class StrategyEngine:
    """
    Executes trading strategies.
    """

    def __init__(self, registry: StrategyRegistry):
        self._registry = registry

    def run(
        self,
        strategy_name: str,
        feature_set: FeatureSet,
    ) -> Signal:
        strategy = self._registry.get(strategy_name)

        return strategy.generate(feature_set)