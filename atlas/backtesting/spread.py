class SpreadModel:
    """
    Applies bid-ask spread to execution prices.
    """

    def __init__(self, spread: float):
        if spread < 0:
            raise ValueError("Spread cannot be negative.")

        self.spread = spread

    def buy_price(self, market_price: float) -> float:
        if market_price <= 0:
            raise ValueError("Market price must be greater than 0.")

        return market_price + self.spread / 2

    def sell_price(self, market_price: float) -> float:
        if market_price <= 0:
            raise ValueError("Market price must be greater than 0.")

        return market_price - self.spread / 2