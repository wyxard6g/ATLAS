from dataclasses import dataclass
from datetime import datetime

from atlas.domain.market_data import MarketData


@dataclass(frozen=True, slots=True)
class FeatureContext:
    """
    Precomputed market data arrays shared by all features.
    """

    market_data: MarketData
    opens: list[float]
    highs: list[float]
    lows: list[float]
    closes: list[float]
    volumes: list[float]
    timestamps: list[datetime]

    @classmethod
    def from_market_data(cls, market_data: MarketData) -> "FeatureContext":
        return cls(
            market_data=market_data,
            opens=[candle.open for candle in market_data.candles],
            highs=[candle.high for candle in market_data.candles],
            lows=[candle.low for candle in market_data.candles],
            closes=[candle.close for candle in market_data.candles],
            volumes=[candle.volume for candle in market_data.candles],
            timestamps=[candle.timestamp for candle in market_data.candles],
        )

    @property
    def count(self) -> int:
        return self.market_data.count

    @property
    def symbol(self) -> str:
        return self.market_data.symbol

    @property
    def timeframe(self) -> str:
        return self.market_data.timeframe