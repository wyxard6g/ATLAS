from datetime import datetime

from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.trade_log import TradeLog
from atlas.domain.signal import Signal
from atlas.domain.trade import Trade, TradeSide


class ExecutionEngine:
    """
    Simulates trade execution during backtesting.
    """

    def __init__(
        self,
        portfolio_manager: PortfolioManager,
        position_manager: PositionManager,
        trade_log: TradeLog,
    ):
        self._portfolio_manager = portfolio_manager
        self._position_manager = position_manager
        self._trade_log = trade_log

    def execute(
        self,
        signal: Signal,
        price: float,
        quantity: float,
    ) -> Trade:

        cost = price * quantity

        self._portfolio_manager.debit_cash(cost)

        self._position_manager.open(
            signal=signal,
            quantity=quantity,
            entry_price=price,
        )

        trade = Trade(
            symbol=signal.symbol,
            side=TradeSide(signal.signal_type.value),
            quantity=quantity,
            price=price,
            timestamp=datetime.now(),
            order_id=f"SIM-{self._trade_log.count + 1}",
        )

        self._trade_log.add(trade)

        return trade