import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData


def test_market_data_creation():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 102, 1000),
        Candle(now + timedelta(minutes=1), 102, 106, 101, 104, 1200),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="memory",
        candles=candles,
    )

    assert market_data.symbol == "EURUSD"
    assert market_data.count == 2
    assert market_data.start_time == now


def test_market_data_rejects_empty_candles():
    with pytest.raises(ValueError):
        MarketData(
            symbol="EURUSD",
            timeframe="1m",
            source="memory",
            candles=[],
        )


def test_market_data_rejects_unsorted_candles():
    now = datetime.now()

    candles = [
        Candle(now + timedelta(minutes=1), 102, 106, 101, 104, 1200),
        Candle(now, 100, 105, 95, 102, 1000),
    ]

    with pytest.raises(ValueError):
        MarketData(
            symbol="EURUSD",
            timeframe="1m",
            source="memory",
            candles=candles,
        )