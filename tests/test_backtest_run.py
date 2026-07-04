from datetime import datetime, timedelta

from atlas.backtesting.engine import BacktestEngine
from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline
from atlas.domain.candle import Candle
from atlas.features.engine import FeatureEngine
from atlas.features.momentum.rsi import RelativeStrengthIndex
from atlas.features.registry import FeatureRegistry
from atlas.features.trend.ema import ExponentialMovingAverage
from atlas.risk.engine import RiskEngine
from atlas.risk.models.minimum_confidence import MinimumConfidenceRiskModel
from atlas.risk.registry import RiskRegistry
from atlas.strategies.engine import StrategyEngine
from atlas.strategies.registry import StrategyRegistry
from atlas.strategies.trend.ema_rsi_strategy import EmaRsiTrendStrategy


def test_backtest_engine_runs_pipeline():
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
    feature_registry.register(RelativeStrengthIndex())

    feature_engine = FeatureEngine(feature_registry)

    feature_pipeline = BacktestFeaturePipeline(
        candles,
        "EURUSD",
        "1m",
        feature_engine,
    )

    strategy_registry = StrategyRegistry()
    strategy_registry.register(EmaRsiTrendStrategy())

    strategy_engine = StrategyEngine(strategy_registry)

    risk_registry = RiskRegistry()
    risk_registry.register(
        MinimumConfidenceRiskModel()
    )

    risk_engine = RiskEngine(risk_registry)

    pipeline = BacktestTradingPipeline(
        feature_pipeline,
        strategy_engine,
        risk_engine,
        "ema_rsi_trend",
        "minimum_confidence",
    )

    engine = BacktestEngine()

    signals = engine.run(
        pipeline,
        start_index=50,
        end_index=59,
    )

    assert len(signals) > 0