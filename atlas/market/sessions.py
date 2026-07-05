from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from zoneinfo import ZoneInfo


class AssetClass(Enum):
    FOREX = "FOREX"
    STOCK = "STOCK"
    CRYPTO = "CRYPTO"
    FUTURES = "FUTURES"


@dataclass(frozen=True, slots=True)
class MarketSession:
    """
    Basic market session checker.
    """

    asset_class: AssetClass
    timezone: str = "UTC"

    def is_market_open(self, current_time: datetime) -> bool:
        local_time = current_time.astimezone(ZoneInfo(self.timezone))

        if self.asset_class == AssetClass.CRYPTO:
            return True

        if self.asset_class == AssetClass.FOREX:
            return self._is_forex_open(local_time)

        if self.asset_class == AssetClass.STOCK:
            return self._is_stock_open(local_time)

        if self.asset_class == AssetClass.FUTURES:
            return self._is_futures_open(local_time)

        return False

    def _is_forex_open(self, current_time: datetime) -> bool:
        weekday = current_time.weekday()

        # Monday-Friday basic FX session rule
        return weekday < 5

    def _is_stock_open(self, current_time: datetime) -> bool:
        weekday = current_time.weekday()

        if weekday >= 5:
            return False

        market_open = time(9, 30)
        market_close = time(16, 0)

        return market_open <= current_time.time() <= market_close

    def _is_futures_open(self, current_time: datetime) -> bool:
        weekday = current_time.weekday()

        # Basic placeholder rule: Sunday-Friday open, Saturday closed
        return weekday != 5