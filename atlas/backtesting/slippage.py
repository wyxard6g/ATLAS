class SlippageModel:
    """
    Applies slippage to execution prices.
    """

    def __init__(self, slippage: float):
        if slippage < 0:
            raise ValueError("Slippage cannot be negative.")

        self.slippage = slippage

    def buy_price(self, execution_price: float) -> float:
        if execution_price <= 0:
            raise ValueError("Execution price must be greater than 0.")

        return execution_price + self.slippage

    def sell_price(self, execution_price: float) -> float:
        if execution_price <= 0:
            raise ValueError("Execution price must be greater than 0.")

        return execution_price - self.slippage