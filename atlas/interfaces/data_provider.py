from abc import ABC, abstractmethod
from datetime import datetime

from atlas.domain.candle import Candle
from atlas.domain.tick import Tick


class DataProvider(ABC):
    """Contract for market data providers."""

    @abstractmethod
    def get_historical_candles(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> list[Candle]:
        pass

    @abstractmethod
    def get_latest_tick(self, symbol: str) -> Tick:
        pass