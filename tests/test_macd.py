import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.momentum.macd import MACD


def test_macd_computation():
    now = datetime.now()

    candles = []

    close = 100

    for i in range(60):
        candles.append(
            Candle(
                timestamp=now + timedelta(minutes=i),
                open=close,
                high=close + 2,
                low=close - 2,
                close=close,
                volume=1000,
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

    macd = MACD()
    result = macd.compute(context)

    assert "macd" in result
    assert "signal" in result
    assert "histogram" in result
    assert isinstance(result["macd"], float)


def test_macd_rejects_invalid_periods():
    with pytest.raises(ValueError):
        MACD(fast_period=26, slow_period=12)


def test_macd_requires_enough_candles():
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

    macd = MACD()

    with pytest.raises(ValueError):
        macd.compute(context)