from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """
    Represents an open portfolio position.
    """

    symbol: str
    quantity: float
    average_price: float
    unrealized_pnl: float = 0.0

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if self.quantity == 0:
            raise ValueError("Quantity cannot be zero.")

        if self.average_price <= 0:
            raise ValueError("Average price must be greater than 0.")