import pytest
from datetime import datetime, timedelta

from atlas.data.memory_provider import MemoryDataProvider
from atlas.domain.candle import Candle


def test_memory_provider_returns_market_data():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 102, 1000),
        Candle(now + timedelta(minutes=1), 102, 106, 101, 104, 1200),
    ]

    provider = MemoryDataProvider(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
    )

    market_data = provider.get_market_data(
        start=now,
        end=now + timedelta(minutes=1),
    )

    assert market_data.count == 2
    assert market_data.symbol == "EURUSD"
    assert market_data.timeframe == "1m"


def test_memory_provider_rejects_empty_candles():
    with pytest.raises(ValueError):
        MemoryDataProvider(
            candles=[],
            symbol="EURUSD",
            timeframe="1m",
        )


def test_memory_provider_latest_tick():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 102, 1000),
    ]

    provider = MemoryDataProvider(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
    )

    tick = provider.get_latest_tick("EURUSD")

    assert tick.symbol == "EURUSD"
    assert tick.price == 102