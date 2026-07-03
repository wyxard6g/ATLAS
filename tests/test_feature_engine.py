from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.engine import FeatureEngine
from atlas.features.registry import FeatureRegistry
from atlas.features.trend.sma import SimpleMovingAverage


def test_feature_engine_returns_feature_set():
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

    registry = FeatureRegistry()
    registry.register(SimpleMovingAverage(period=3))

    engine = FeatureEngine(registry)

    feature_set = engine.compute(market_data)

    assert feature_set.symbol == "EURUSD"
    assert feature_set.timeframe == "1m"
    assert feature_set.get("sma_3") == 102