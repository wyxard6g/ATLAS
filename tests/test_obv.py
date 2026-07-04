import pytest
from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext
from atlas.features.volume.obv import OnBalanceVolume


def test_obv_computation():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 100, 1000),
        Candle(now + timedelta(minutes=1), 100, 106, 96, 102, 1200),
        Candle(now + timedelta(minutes=2), 102, 107, 97, 101, 800),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)

    obv = OnBalanceVolume()

    assert obv.compute(context) == 400


def test_obv_requires_enough_candles():
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

    obv = OnBalanceVolume()

    with pytest.raises(ValueError):
        obv.compute(context)