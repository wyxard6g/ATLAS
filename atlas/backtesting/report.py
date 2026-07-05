from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BacktestReport:
    """
    Represents the outcome of a completed backtest.
    """

    starting_capital: float
    ending_capital: float
    total_return: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    maximum_drawdown: float = 0.0
    profit_factor: float = 0.0
    sharpe_ratio: float = 0.0

    def __str__(self) -> str:
        return (
            "\n"
            "========================================\n"
            "          ATLAS BACKTEST REPORT\n"
            "========================================\n"
            f"Starting Capital : {self.starting_capital:,.2f}\n"
            f"Ending Capital   : {self.ending_capital:,.2f}\n"
            f"Total Return     : {self.total_return:,.2f}\n"
            f"Trades           : {self.total_trades}\n"
            f"Wins             : {self.winning_trades}\n"
            f"Losses           : {self.losing_trades}\n"
            f"Win Rate         : {self.win_rate:.2%}\n"
            f"Max Drawdown     : {self.maximum_drawdown:.2%}\n"
            f"Profit Factor    : {self.profit_factor:.2f}\n"
            f"Sharpe Ratio     : {self.sharpe_ratio:.2f}\n"
            "========================================"
        )