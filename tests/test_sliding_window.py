from datetime import datetime, timedelta

import pytest

from atlas.backtesting.window import SlidingWindowBuilder
from atlas.domain.candle import Candle


def test_sliding_window_builds_market_data():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 101, 1000),
        Candle(now + timedelta(minutes=1), 101, 106, 100, 103, 1100),
        Candle(now + timedelta(minutes=2), 103, 107, 102, 104, 1200),
    ]

    builder = SlidingWindowBuilder(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
    )

    market_data = builder.build(end_index=1)

    assert market_data.count == 2
    assert market_data.symbol == "EURUSD"
    assert market_data.end_time == candles[1].timestamp


def test_sliding_window_rejects_empty_input():
    with pytest.raises(ValueError):
        SlidingWindowBuilder([], symbol="EURUSD", timeframe="1m")


def test_sliding_window_rejects_invalid_index():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 101, 1000),
    ]

    builder = SlidingWindowBuilder(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
    )

    with pytest.raises(ValueError):
        builder.build(end_index=10)