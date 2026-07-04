from atlas.backtesting.pipeline import BacktestFeaturePipeline
from atlas.domain.signal import Signal
from atlas.features.engine import FeatureEngine
from atlas.risk.engine import RiskEngine
from atlas.strategies.engine import StrategyEngine


class BacktestTradingPipeline:
    """
    Executes the complete trading decision pipeline.
    """

    def __init__(
        self,
        feature_pipeline: BacktestFeaturePipeline,
        strategy_engine: StrategyEngine,
        risk_engine: RiskEngine,
        strategy_name: str,
        risk_model_name: str,
    ):
        self._feature_pipeline = feature_pipeline
        self._strategy_engine = strategy_engine
        self._risk_engine = risk_engine
        self._strategy_name = strategy_name
        self._risk_model_name = risk_model_name

    def evaluate(self, candle_index: int) -> tuple[Signal, bool]:
        feature_set = self._feature_pipeline.compute_at(candle_index)

        signal = self._strategy_engine.run(
            self._strategy_name,
            feature_set,
        )

        approved = self._risk_engine.evaluate(
            self._risk_model_name,
            signal,
        )

        return signal, approved