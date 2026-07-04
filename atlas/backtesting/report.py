from atlas.backtesting.statistics import Statistics


class BacktestReport:
    """
    Summary report for a completed backtest.
    """

    def __init__(self, statistics: Statistics):
        self.statistics = statistics

    def summary(self) -> dict:
        return {
            "total_trades": self.statistics.total_trades,
        }