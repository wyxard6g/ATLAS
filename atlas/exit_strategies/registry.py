from atlas.exit_strategies.base import ExitStrategy


class ExitStrategyRegistry:
    """
    Stores available exit strategies.
    """

    def __init__(self):
        self._strategies: dict[str, ExitStrategy] = {}

    def register(self, strategy: ExitStrategy) -> None:
        self._strategies[strategy.name] = strategy

    def get(self, name: str) -> ExitStrategy:
        return self._strategies[name]