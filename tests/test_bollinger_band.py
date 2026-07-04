import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.volatility.bollinger_bands import BollingerBands


def test_bollinger_bands_computation():
    now = datetime.now()

    candles = []

    for i in range(30):
        close = 100 + i

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

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)

    bands = BollingerBands(period=20)
    result = bands.compute(context)

    assert "middle" in result
    assert "upper" in result
    assert "lower" in result
    assert "width" in result
    assert result["upper"] > result["middle"]
    assert result["lower"] < result["middle"]


def test_bollinger_bands_rejects_invalid_period():
    with pytest.raises(ValueError):
        BollingerBands(period=0)


def test_bollinger_bands_requires_enough_candles():
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

    bands = BollingerBands(period=20)

    with pytest.raises(ValueError):
        bands.compute(context)