from atlas.backtesting.entry_engine import EntryEngine
from atlas.backtesting.equity_curve import EquityCurve
from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.position_manager import PositionManager
from atlas.domain.signal import Signal, SignalType
from atlas.risk.position_sizing import PositionSizingEngine


class TradeLifecycleManager:
    """
    Orchestrates simulated trade entries, exits, and equity tracking.
    """

    def __init__(
        self,
        entry_engine: EntryEngine,
        exit_engine: ExitEngine,
        position_manager: PositionManager,
        equity_curve: EquityCurve,
        position_sizing_engine: PositionSizingEngine,
    ):
        self._entry_engine = entry_engine
        self._exit_engine = exit_engine
        self._positions = position_manager
        self._equity_curve = equity_curve
        self._position_sizing_engine = position_sizing_engine

    def process_entry(
        self,
        signal: Signal,
        price: float,
        stop_loss_price: float,
        account_equity: float,
    ) -> bool:
        if signal.signal_type == SignalType.HOLD:
            return False

        if self._positions.has_position(signal.symbol):
            return False

        quantity = self._position_sizing_engine.calculate_size(
            account_equity=account_equity,
            entry_price=price,
            stop_loss_price=stop_loss_price,
        )

        self._entry_engine.open(
            signal=signal,
            entry_price=price,
            quantity=quantity,
        )

        return True

    def process_exit(
        self,
        symbol: str,
        price: float,
    ) -> float:
        return self._exit_engine.close(
            symbol=symbol,
            exit_price=price,
        )