from atlas.backtesting.candle_processor import CandleProcessor
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.domain.candle import Candle
from atlas.domain.signal import Signal


class FullBacktestRunner:
    """
    Runs a complete candle-by-candle backtest.
    """

    def __init__(
        self,
        candles: list[Candle],
        candle_processor: CandleProcessor,
        portfolio_manager: PortfolioManager,
        start_index: int,
    ):
        if not candles:
            raise ValueError("Candles cannot be empty.")

        if start_index < 0 or start_index >= len(candles):
            raise ValueError("Start index is out of range.")

        self._candles = candles
        self._processor = candle_processor
        self._portfolio = portfolio_manager
        self._start_index = start_index

    def run(self) -> list[tuple[Signal, bool]]:
        results = []

        for index in range(self._start_index, len(self._candles)):
            candle = self._candles[index]

            result = self._processor.process(
                candle=candle,
                candle_index=index,
                account_equity=self._portfolio.equity,
            )

            results.append(result)

        return results