class CommissionModel:
    """
    Calculates trading commission.
    """

    def __init__(self, rate: float = 0.001):
        if rate < 0:
            raise ValueError("Commission rate cannot be negative.")

        self.rate = rate

    def calculate(self, trade_value: float) -> float:
        if trade_value < 0:
            raise ValueError("Trade value cannot be negative.")

        return trade_value * self.rate