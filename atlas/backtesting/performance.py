class PerformanceStatistics:
    """
    Computes basic performance metrics from completed trades.
    """

    def __init__(self, trade_pnls: list[float]):
        self._pnls = trade_pnls

    @property
    def total_return(self) -> float:
        return sum(self._pnls)

    @property
    def total_trades(self) -> int:
        return len(self._pnls)

    @property
    def winning_trades(self) -> int:
        return sum(1 for pnl in self._pnls if pnl > 0)

    @property
    def losing_trades(self) -> int:
        return sum(1 for pnl in self._pnls if pnl < 0)

    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0

        return self.winning_trades / self.total_trades