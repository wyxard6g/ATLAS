import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.volatility.atr import AverageTrueRange


def test_atr_computation():
    now = datetime.now()

    candles = []

    for i in range(20):
        candles.append(
            Candle(
                timestamp=now + timedelta(minutes=i),
                open=100 + i,
                high=105 + i,
                low=95 + i,
                close=102 + i,
                volume=1000,
            )
        )

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    atr = AverageTrueRange(period=14)

    value = atr.compute(context)

    assert isinstance(value, float)
    assert value > 0


def test_atr_rejects_invalid_period():
    with pytest.raises(ValueError):
        AverageTrueRange(period=0)


def test_atr_requires_enough_candles():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 102, 1000),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)
    atr = AverageTrueRange(period=14)

    with pytest.raises(ValueError):
        atr.compute(context)