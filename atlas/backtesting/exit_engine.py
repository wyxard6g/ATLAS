from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.domain.position import Position


class ExitEngine:
    """
    Handles closing simulated positions.
    """

    def __init__(
        self,
        portfolio_manager: PortfolioManager,
        position_manager: PositionManager,
    ):
        self._portfolio = portfolio_manager
        self._positions = position_manager

    def close(
        self,
        symbol: str,
        exit_price: float,
    ) -> float:

        position = self._positions.close(symbol)

        proceeds = position.quantity * exit_price

        self._portfolio.credit_cash(proceeds)

        pnl = (
            exit_price - position.average_price
        ) * position.quantity

        return pnl