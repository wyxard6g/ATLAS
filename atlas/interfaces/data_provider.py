from abc import ABC, abstractmethod
from datetime import datetime

from atlas.domain.market_data import MarketData
from atlas.domain.tick import Tick


class DataProvider(ABC):
    """
    Contract for market data providers.
    """

    @abstractmethod
    def get_market_data(
        self,
        start: datetime,
        end: datetime,
    ) -> MarketData:
        """
        Return validated market data.
        """
        pass

    @abstractmethod
    def get_latest_tick(
        self,
        symbol: str,
    ) -> Tick:
        """
        Return latest market tick.
        """
        pass