from datetime import datetime, timedelta

from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline
from atlas.domain.candle import Candle
from atlas.features.engine import FeatureEngine
from atlas.features.registry import FeatureRegistry
from atlas.features.trend.ema import ExponentialMovingAverage
from atlas.features.momentum.rsi import RelativeStrengthIndex
from atlas.risk.engine import RiskEngine
from atlas.risk.models.minimum_confidence import MinimumConfidenceRiskModel
from atlas.risk.registry import RiskRegistry
from atlas.strategies.engine import StrategyEngine
from atlas.strategies.registry import StrategyRegistry
from atlas.strategies.trend.ema_rsi_strategy import EmaRsiTrendStrategy


def test_complete_trading_pipeline():
    now = datetime.now()

    candles = []

    close = 100

    for i in range(60):
        candles.append(
            Candle(
                now + timedelta(minutes=i),
                close,
                close + 2,
                close - 2,
                close,
                1000,
            )
        )
        close += 1

    feature_registry = FeatureRegistry()
    feature_registry.register(ExponentialMovingAverage(20))
    feature_registry.register(ExponentialMovingAverage(50))
    feature_registry.register(RelativeStrengthIndex(14))

    feature_engine = FeatureEngine(feature_registry)

    feature_pipeline = BacktestFeaturePipeline(
        candles=candles,
        symbol="EURUSD",
        timeframe="1m",
        feature_engine=feature_engine,
    )

    strategy_registry = StrategyRegistry()
    strategy_registry.register(EmaRsiTrendStrategy())

    strategy_engine = StrategyEngine(strategy_registry)

    risk_registry = RiskRegistry()
    risk_registry.register(
        MinimumConfidenceRiskModel(0.60)
    )

    risk_engine = RiskEngine(risk_registry)

    pipeline = BacktestTradingPipeline(
        feature_pipeline=feature_pipeline,
        strategy_engine=strategy_engine,
        risk_engine=risk_engine,
        strategy_name="ema_rsi_trend",
        risk_model_name="minimum_confidence",
    )

    signal, approved = pipeline.evaluate(59)

    assert approved is True
    assert signal.confidence >= 0.60
    