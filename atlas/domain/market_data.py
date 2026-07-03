from dataclasses import dataclass, field
from datetime import datetime

from atlas.domain.candle import Candle


@dataclass(frozen=True, slots=True)
class MarketData:
    """
    Represents a validated collection of market candles plus metadata.
    """

    symbol: str
    timeframe: str
    source: str
    candles: list[Candle]
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if not self.timeframe.strip():
            raise ValueError("Timeframe cannot be empty.")

        if not self.source.strip():
            raise ValueError("Source cannot be empty.")

        if not self.candles:
            raise ValueError("MarketData must contain at least one candle.")

        timestamps = [candle.timestamp for candle in self.candles]

        if timestamps != sorted(timestamps):
            raise ValueError("Candles must be sorted by timestamp.")

    @property
    def start_time(self) -> datetime:
        return self.candles[0].timestamp

    @property
    def end_time(self) -> datetime:
        return self.candles[-1].timestamp

    @property
    def count(self) -> int:
        return len(self.candles)