from datetime import datetime

from atlas.backtesting.entry_engine import EntryEngine
from atlas.backtesting.equity_curve import EquityCurve
from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.lifecycle_manager import TradeLifecycleManager
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.trade_log import TradeLog
from atlas.domain.signal import Signal, SignalType
from atlas.risk.position_sizing import PositionSizingEngine


def make_signal(signal_type: SignalType) -> Signal:
    return Signal(
        symbol="EURUSD",
        signal_type=signal_type,
        confidence=0.9,
        timeframe="1m",
        strategy="test",
        timestamp=datetime.now(),
        reason="unit test",
    )


def make_lifecycle_manager():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()
    trades = TradeLog()
    equity_curve = EquityCurve()
    position_sizing = PositionSizingEngine(risk_per_trade=0.01)

    entry_engine = EntryEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
        trade_log=trades,
    )

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    lifecycle = TradeLifecycleManager(
        entry_engine=entry_engine,
        exit_engine=exit_engine,
        position_manager=positions,
        equity_curve=equity_curve,
        position_sizing_engine=position_sizing,
    )

    return lifecycle, positions, portfolio


def test_lifecycle_manager_opens_position_with_risk_based_size():
    lifecycle, positions, portfolio = make_lifecycle_manager()

    opened = lifecycle.process_entry(
        signal=make_signal(SignalType.BUY),
        price=100,
        stop_loss_price=95,
        account_equity=100_000,
    )

    position = positions.get("EURUSD")

    assert opened is True
    assert positions.count == 1
    assert position is not None
    assert position.quantity == 200
    assert portfolio.cash == 80_000


def test_lifecycle_manager_ignores_hold_signal():
    lifecycle, positions, portfolio = make_lifecycle_manager()

    opened = lifecycle.process_entry(
        signal=make_signal(SignalType.HOLD),
        price=100,
        stop_loss_price=95,
        account_equity=100_000,
    )

    assert opened is False
    assert positions.count == 0
    assert portfolio.cash == 100_000


def test_lifecycle_manager_prevents_duplicate_position():
    lifecycle, positions, portfolio = make_lifecycle_manager()

    lifecycle.process_entry(
        signal=make_signal(SignalType.BUY),
        price=100,
        stop_loss_price=95,
        account_equity=100_000,
    )

    opened = lifecycle.process_entry(
        signal=make_signal(SignalType.BUY),
        price=101,
        stop_loss_price=96,
        account_equity=100_000,
    )

    assert opened is False
    assert positions.count == 1
    assert portfolio.cash == 80_000


def test_lifecycle_manager_closes_position():
    lifecycle, positions, portfolio = make_lifecycle_manager()

    lifecycle.process_entry(
        signal=make_signal(SignalType.BUY),
        price=100,
        stop_loss_price=95,
        account_equity=100_000,
    )

    pnl = lifecycle.process_exit(
        symbol="EURUSD",
        price=110,
    )

    assert pnl == 2000
    assert positions.count == 0
    assert portfolio.cash == 102_000