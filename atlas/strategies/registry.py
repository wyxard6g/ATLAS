from atlas.strategies.base import Strategy


class StrategyRegistry:
    """
    Stores all available strategies.
    """

    def __init__(self):
        self._strategies: dict[str, Strategy] = {}

    def register(self, strategy: Strategy):
        self._strategies[strategy.name] = strategy

    def get(self, name: str) -> Strategy:
        return self._strategies[name]

    def all(self):
        return list(self._strategies.values())