from datetime import datetime

from atlas.backtesting.entry_engine import EntryEngine
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.trade_log import TradeLog
from atlas.domain.signal import Signal, SignalType


def test_entry_engine_opens_position_and_records_trade():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()
    trades = TradeLog()

    engine = EntryEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
        trade_log=trades,
    )

    signal = Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.9,
        timeframe="1m",
        strategy="test",
        timestamp=datetime.now(),
        reason="unit test",
    )

    trade = engine.open(
        signal=signal,
        entry_price=100,
        quantity=10,
    )

    assert trade.symbol == "EURUSD"
    assert trades.count == 1
    assert positions.count == 1
    assert portfolio.cash == 99_000