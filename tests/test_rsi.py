import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.momentum.rsi import RelativeStrengthIndex


def test_rsi_returns_float():
    now = datetime.now()

    candles = []
    close = 100

    for i in range(20):
        candles.append(
            Candle(
                now + timedelta(minutes=i),
                close,
                close + 1,
                close - 1,
                close,
                1000,
            )
        )
        close += 1

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    rsi = RelativeStrengthIndex(14)

    value = rsi.compute(context)

    assert isinstance(value, float)
    assert 0 <= value <= 100


def test_invalid_period():
    with pytest.raises(ValueError):
        RelativeStrengthIndex(0)


def test_not_enough_candles():
    now = datetime.now()

    candles = [
        Candle(now, 100, 101, 99, 100, 1000),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    rsi = RelativeStrengthIndex()

    with pytest.raises(ValueError):
        rsi.compute(context)