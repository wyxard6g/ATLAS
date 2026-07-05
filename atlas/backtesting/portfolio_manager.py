from atlas.backtesting.portfolio import Portfolio


class PortfolioManager:
    """
    Manages cash and equity during backtesting.
    """

    def __init__(self, starting_cash: float):
        if starting_cash <= 0:
            raise ValueError("Starting cash must be greater than 0.")

        self.portfolio = Portfolio(
            cash=starting_cash,
            equity=starting_cash,
        )

    def debit_cash(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Debit amount must be greater than 0.")

        if amount > self.portfolio.cash:
            raise ValueError("Insufficient cash.")

        self.portfolio.cash -= amount
        self.portfolio.equity = self.portfolio.cash

    def credit_cash(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Credit amount must be greater than 0.")

        self.portfolio.cash += amount
        self.portfolio.equity = self.portfolio.cash

    @property
    def cash(self) -> float:
        return self.portfolio.cash

    @property
    def equity(self) -> float:
        return self.portfolio.equity