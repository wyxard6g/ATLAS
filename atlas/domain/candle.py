from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Candle:
    """
    Represents one OHLCV market candle.

    Immutable and validated.
    """

    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: float

    def __post_init__(self):
        """
        Validate candle integrity.
        """

        if self.high < self.low:
            raise ValueError("High price cannot be lower than low price.")

        if self.open > self.high or self.open < self.low:
            raise ValueError("Open price must be between low and high.")

        if self.close > self.high or self.close < self.low:
            raise ValueError("Close price must be between low and high.")

        if self.volume < 0:
            raise ValueError("Volume cannot be negative.")