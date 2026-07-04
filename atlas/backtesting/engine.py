from atlas.backtesting.portfolio import Portfolio
from atlas.backtesting.report import BacktestReport
from atlas.backtesting.statistics import Statistics
from atlas.backtesting.trade_log import TradeLog


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

    def report(self) -> BacktestReport:
        stats = Statistics(self.trade_log)
        return BacktestReport(stats)