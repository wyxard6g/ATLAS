from atlas.domain.position import Position
from atlas.exit_strategies.registry import ExitStrategyRegistry


class ExitStrategyEngine:
    """
    Evaluates exit strategies.
    """

    def __init__(self, registry: ExitStrategyRegistry):
        self._registry = registry

    def should_exit(
        self,
        strategy_name: str,
        position: Position,
        current_price: float,
    ) -> bool:
        strategy = self._registry.get(strategy_name)

        return strategy.should_exit(
            position=position,
            current_price=current_price,
        )