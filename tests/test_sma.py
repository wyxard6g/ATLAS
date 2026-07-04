import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.trend.sma import SimpleMovingAverage


def test_sma_computation():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 100, 1000),
        Candle(now + timedelta(minutes=1), 100, 106, 96, 102, 1000),
        Candle(now + timedelta(minutes=2), 102, 107, 97, 104, 1000),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    sma = SimpleMovingAverage(period=3)

    assert sma.compute(context) == 102


def test_sma_rejects_invalid_period():
    with pytest.raises(ValueError):
        SimpleMovingAverage(period=0)


def test_sma_requires_enough_candles():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 100, 1000),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    sma = SimpleMovingAverage(period=3)

    with pytest.raises(ValueError):
        sma.compute(context)