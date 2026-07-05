from datetime import datetime, timedelta

from atlas.backtesting.candle_processor import CandleProcessor
from atlas.backtesting.entry_engine import EntryEngine
from atlas.backtesting.equity_curve import EquityCurve
from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.lifecycle_manager import TradeLifecycleManager
from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.trade_log import TradeLog
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline
from atlas.domain.candle import Candle
from atlas.domain.signal import SignalType
from atlas.features.engine import FeatureEngine
from atlas.features.momentum.rsi import RelativeStrengthIndex
from atlas.features.registry import FeatureRegistry
from atlas.features.trend.ema import ExponentialMovingAverage
from atlas.risk.engine import RiskEngine
from atlas.risk.models.minimum_confidence import MinimumConfidenceRiskModel
from atlas.risk.position_sizing import PositionSizingEngine
from atlas.risk.registry import RiskRegistry
from atlas.strategies.engine import StrategyEngine
from atlas.strategies.registry import StrategyRegistry
from atlas.strategies.trend.ema_rsi_strategy import EmaRsiTrendStrategy


def test_candle_processor_opens_trade_from_approved_signal():
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
    risk_registry.register(MinimumConfidenceRiskModel(0.60))

    risk_engine = RiskEngine(risk_registry)

    trading_pipeline = BacktestTradingPipeline(
        feature_pipeline=feature_pipeline,
        strategy_engine=strategy_engine,
        risk_engine=risk_engine,
        strategy_name="ema_rsi_trend",
        risk_model_name="minimum_confidence",
    )

    portfolio = PortfolioManager(100_000)
    positions = PositionManager()
    trades = TradeLog()
    equity_curve = EquityCurve()
    sizing = PositionSizingEngine(risk_per_trade=0.01)

    entry_engine = EntryEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
        trade_log=trades,
    )

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    lifecycle = TradeLifecycleManager(
        entry_engine=entry_engine,
        exit_engine=exit_engine,
        position_manager=positions,
        equity_curve=equity_curve,
        position_sizing_engine=sizing,
    )

    processor = CandleProcessor(
        trading_pipeline=trading_pipeline,
        lifecycle_manager=lifecycle,
        stop_loss_percent=0.05,
    )

    signal, opened = processor.process(
        candle=candles[59],
        candle_index=59,
        account_equity=portfolio.equity,
    )

    assert signal.signal_type == SignalType.BUY
    assert opened is True
    assert positions.count == 1
    assert trades.count == 1