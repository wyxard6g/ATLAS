from datetime import datetime

import pytest

from atlas.backtesting.position_manager import PositionManager
from atlas.domain.signal import Signal, SignalType


def make_signal(signal_type=SignalType.BUY):
    return Signal(
        symbol="EURUSD",
        signal_type=signal_type,
        confidence=0.9,
        timeframe="1m",
        strategy="test",
        timestamp=datetime.now(),
        reason="unit test",
    )


def test_open_position():
    manager = PositionManager()

    position = manager.open(
        signal=make_signal(),
        quantity=1.0,
        entry_price=100.0,
    )

    assert manager.count == 1
    assert position.symbol == "EURUSD"
    assert position.average_price == 100.0


def test_cannot_open_duplicate_position():
    manager = PositionManager()

    manager.open(
        signal=make_signal(),
        quantity=1.0,
        entry_price=100.0,
    )

    with pytest.raises(ValueError):
        manager.open(
            signal=make_signal(),
            quantity=1.0,
            entry_price=101.0,
        )


def test_close_position():
    manager = PositionManager()

    manager.open(
        signal=make_signal(),
        quantity=1.0,
        entry_price=100.0,
    )

    closed = manager.close("EURUSD")

    assert closed.symbol == "EURUSD"
    assert manager.count == 0


def test_close_nonexistent_position():
    manager = PositionManager()

    with pytest.raises(ValueError):
        manager.close("EURUSD")