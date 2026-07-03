import pytest
from datetime import datetime, timedelta

from atlas.data.memory_provider import MemoryDataProvider
from atlas.domain.candle import Candle


def test_memory_provider_returns_candles():
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

    result = provider.get_historical_candles(
        symbol="EURUSD",
        start=now,
        end=now + timedelta(minutes=1),
        timeframe="1m",
    )

    assert len(result) == 2


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