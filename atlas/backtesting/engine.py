from atlas.backtesting.portfolio import Portfolio
from atlas.backtesting.report import BacktestReport
from atlas.backtesting.statistics import Statistics
from atlas.backtesting.trade_log import TradeLog
from atlas.backtesting.trading_pipeline import BacktestTradingPipeline


class BacktestEngine:
    """
    Executes historical simulations.
    """

    def __init__(self, starting_cash: float = 100_000):
        self.portfolio = Portfolio(
            cash=starting_cash,
            equity=starting_cash,
        )

        self.trade_log = TradeLog()

    def run(
        self,
        pipeline: BacktestTradingPipeline,
        start_index: int,
        end_index: int,
    ):
        """
        Replay historical candles through the trading pipeline.
        """

        approved_signals = []

        for i in range(start_index, end_index + 1):

            signal, approved = pipeline.evaluate(i)

            if approved:
                approved_signals.append(signal)

        return approved_signals

    def report(self) -> BacktestReport:
        stats = Statistics(self.trade_log)

        return BacktestReport(stats)