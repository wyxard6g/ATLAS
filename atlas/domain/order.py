from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


@dataclass(frozen=True, slots=True)
class Order:
    """
    Represents an order request before it is sent to a broker.
    """

    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    timestamp: datetime
    limit_price: float | None = None
    stop_price: float | None = None

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if self.order_type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError("Limit orders require a limit price.")

        if self.order_type == OrderType.STOP and self.stop_price is None:
            raise ValueError("Stop orders require a stop price.")