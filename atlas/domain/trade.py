from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TradeSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class Trade:
    """
    Represents an executed order.
    """

    symbol: str
    side: TradeSide
    quantity: float
    price: float
    timestamp: datetime
    order_id: str

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if self.price <= 0:
            raise ValueError("Execution price must be greater than 0.")

        if not self.order_id.strip():
            raise ValueError("Order ID cannot be empty.")