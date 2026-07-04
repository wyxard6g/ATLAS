from atlas.backtesting.trade_log import TradeLog


class Statistics:
    """
    Computes simple backtest statistics.
    """

    def __init__(self, trade_log: TradeLog):
        self.trade_log = trade_log

    @property
    def total_trades(self) -> int:
        return self.trade_log.count