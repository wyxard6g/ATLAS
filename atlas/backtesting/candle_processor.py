from atlas.backtesting.lifecycle_manager import TradeLifecycleManager
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline
from atlas.domain.candle import Candle
from atlas.domain.signal import Signal


class CandleProcessor:
    """
    Processes one historical candle through the trading pipeline.
    """

    def __init__(
        self,
        trading_pipeline: BacktestTradingPipeline,
        lifecycle_manager: TradeLifecycleManager,
        stop_loss_percent: float = 0.05,
    ):
        if stop_loss_percent <= 0:
            raise ValueError("Stop loss percent must be greater than 0.")

        self._trading_pipeline = trading_pipeline
        self._lifecycle = lifecycle_manager
        self._stop_loss_percent = stop_loss_percent

    def process(
        self,
        candle: Candle,
        candle_index: int,
        account_equity: float,
    ) -> tuple[Signal, bool]:
        signal, approved = self._trading_pipeline.evaluate(candle_index)

        if not approved:
            return signal, False

        stop_loss_price = candle.close * (1 - self._stop_loss_percent)

        opened = self._lifecycle.process_entry(
            signal=signal,
            price=candle.close,
            stop_loss_price=stop_loss_price,
            account_equity=account_equity,
        )

        return signal, opened