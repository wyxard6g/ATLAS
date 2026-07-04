from dataclasses import dataclass


@dataclass
class Portfolio:
    """
    Represents portfolio state during backtesting.
    """

    cash: float
    equity: float
    positions: int = 0

    def update_equity(self, value: float) -> None:
        self.equity = value