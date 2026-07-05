from datetime import datetime

from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.trade_log import TradeLog
from atlas.domain.signal import Signal
from atlas.domain.trade import Trade, TradeSide


class EntryEngine:
    """
    Handles opening simulated positions.
    """

    def __init__(
        self,
        portfolio_manager: PortfolioManager,
        position_manager: PositionManager,
        trade_log: TradeLog,
    ):
        self._portfolio = portfolio_manager
        self._positions = position_manager
        self._trade_log = trade_log

    def open(
        self,
        signal: Signal,
        entry_price: float,
        quantity: float,
    ) -> Trade:
        cost = entry_price * quantity

        self._portfolio.debit_cash(cost)

        self._positions.open(
            signal=signal,
            quantity=quantity,
            entry_price=entry_price,
        )

        trade = Trade(
            symbol=signal.symbol,
            side=TradeSide(signal.signal_type.value),
            quantity=quantity,
            price=entry_price,
            timestamp=datetime.now(),
            order_id=f"ENTRY-{self._trade_log.count + 1}",
        )

        self._trade_log.add(trade)

        return trade