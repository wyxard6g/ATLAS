from datetime import datetime, timedelta

from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.domain.candle import Candle
from atlas.features.engine import FeatureEngine
from atlas.features.registry import FeatureRegistry
from atlas.features.trend.sma import SimpleMovingAverage


def test_backtest_feature_pipeline_computes_features():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 100, 1000),
        Candle(now + timedelta(minutes=1), 100, 106, 96, 102, 1000),
        Candle(now + timedelta(minutes=2), 102, 107, 97, 104, 1000),
    ]

    registry = FeatureRegistry()
    registry.register(SimpleMovingAverage(period=3))

    feature_engine = FeatureEngine(registry)

    pipeline = BacktestFeaturePipeline(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
        feature_engine=feature_engine,
    )

    feature_set = pipeline.compute_at(end_index=2)

    assert feature_set.symbol == "EURUSD"
    assert feature_set.get("sma_3") == 102