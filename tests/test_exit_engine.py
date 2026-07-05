from datetime import datetime

from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.domain.signal import Signal, SignalType


def make_signal():
    return Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.9,
        timeframe="1m",
        strategy="test",
        timestamp=datetime.now(),
        reason="unit test",
    )


def test_exit_engine_closes_position_and_returns_profit():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()

    positions.open(
        signal=make_signal(),
        quantity=10,
        entry_price=100,
    )

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    pnl = exit_engine.close(
        symbol="EURUSD",
        exit_price=110,
    )

    assert pnl == 100
    assert positions.count == 0