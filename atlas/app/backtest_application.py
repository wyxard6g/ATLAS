from pathlib import Path

from atlas.backtesting.candle_processor import CandleProcessor
from atlas.backtesting.entry_engine import EntryEngine
from atlas.backtesting.equity_curve import EquityCurve
from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.full_runner import FullBacktestRunner
from atlas.backtesting.lifecycle_manager import TradeLifecycleManager
from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.position_monitor import PositionMonitor
from atlas.backtesting.report import BacktestReport
from atlas.backtesting.trade_log import TradeLog
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline
from atlas.data.csv_loader import CSVLoader
from atlas.exit_strategies.engine import ExitStrategyEngine
from atlas.exit_strategies.fixed_percent import FixedPercentExitStrategy
from atlas.exit_strategies.registry import ExitStrategyRegistry
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


class BacktestApplication:
    """
    High-level application entry point for running backtests.
    """

    def __init__(self, starting_capital: float = 100_000):
        if starting_capital <= 0:
            raise ValueError("Starting capital must be greater than 0.")

        self.starting_capital = starting_capital
        self.csv_loader = CSVLoader()

    def run(self, csv_path: str) -> BacktestReport:
        self.validate_file(csv_path)

        candles = self.csv_loader.load(csv_path)

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

        portfolio = PortfolioManager(self.starting_capital)
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

        exit_registry = ExitStrategyRegistry()
        exit_registry.register(
            FixedPercentExitStrategy(
                take_profit_percent=0.10,
                stop_loss_percent=0.05,
            )
        )

        exit_strategy_engine = ExitStrategyEngine(exit_registry)

        monitor = PositionMonitor(
            position_manager=positions,
            exit_strategy_engine=exit_strategy_engine,
            exit_engine=exit_engine,
            exit_strategy_name="fixed_percent",
        )

        start_index = min(50, len(candles) - 1)

        runner = FullBacktestRunner(
            candles=candles,
            candle_processor=processor,
            portfolio_manager=portfolio,
            position_monitor=monitor,
            start_index=start_index,
        )

        runner.run()

        ending_capital = portfolio.equity

        return BacktestReport(
            starting_capital=self.starting_capital,
            ending_capital=ending_capital,
            total_return=ending_capital - self.starting_capital,
            total_trades=trades.count,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
        )

    def validate_file(self, csv_path: str) -> None:
        path = Path(csv_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        if path.suffix.lower() != ".csv":
            raise ValueError("Backtest input must be a CSV file.")