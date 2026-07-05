from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.position_manager import PositionManager
from atlas.exit_strategies.engine import ExitStrategyEngine


class PositionMonitor:
    """
    Monitors open positions and closes them when exit rules trigger.
    """

    def __init__(
        self,
        position_manager: PositionManager,
        exit_strategy_engine: ExitStrategyEngine,
        exit_engine: ExitEngine,
        exit_strategy_name: str,
    ):
        self._positions = position_manager
        self._exit_strategy_engine = exit_strategy_engine
        self._exit_engine = exit_engine
        self._exit_strategy_name = exit_strategy_name

    def check_exit(
        self,
        symbol: str,
        current_price: float,
    ) -> float | None:
        position = self._positions.get(symbol)

        if position is None:
            return None

        should_exit = self._exit_strategy_engine.should_exit(
            strategy_name=self._exit_strategy_name,
            position=position,
            current_price=current_price,
        )

        if not should_exit:
            return None

        return self._exit_engine.close(
            symbol=symbol,
            exit_price=current_price,
        )