import pytest
from datetime import datetime

from atlas.domain.signal import Signal, SignalType


def test_signal_creation():
    signal = Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.92,
        timeframe="1H",
        strategy="TrendFollowing",
        timestamp=datetime.now(),
        reason="Trend and momentum aligned",
    )

    assert signal.signal_type == SignalType.BUY
    assert signal.confidence == 0.92


def test_invalid_confidence():
    with pytest.raises(ValueError):
        Signal(
            symbol="EURUSD",
            signal_type=SignalType.BUY,
            confidence=1.5,
            timeframe="1H",
            strategy="TrendFollowing",
            timestamp=datetime.now(),
            reason="Test",
        )


def test_empty_symbol():
    with pytest.raises(ValueError):
        Signal(
            symbol="",
            signal_type=SignalType.BUY,
            confidence=0.9,
            timeframe="1H",
            strategy="TrendFollowing",
            timestamp=datetime.now(),
            reason="Test",
        )