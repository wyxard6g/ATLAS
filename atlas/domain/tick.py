from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Tick:
    """
    Represents a single market tick (real-time price update).
    """

    symbol: str
    price: float
    volume: float
    timestamp: datetime

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if self.price <= 0:
            raise ValueError("Price must be greater than 0.")

        if self.volume < 0:
            raise ValueError("Volume cannot be negative.")