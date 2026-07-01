from datetime import datetime

from atlas.data.validators import validate_candles
from atlas.domain.candle import Candle
from atlas.domain.tick import Tick
from atlas.interfaces.data_provider import DataProvider


class MemoryDataProvider(DataProvider):
    """
    In-memory market data provider for testing and development.
    """

    def __init__(self, candles: list[Candle]):
        validate_candles(candles)
        self._candles = candles

    def get_historical_candles(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> list[Candle]:
        return [
            candle
            for candle in self._candles
            if start <= candle.timestamp <= end
        ]

    def get_latest_tick(self, symbol: str) -> Tick:
        latest = self._candles[-1]

        return Tick(
            symbol=symbol,
            price=latest.close,
            volume=latest.volume,
            timestamp=latest.timestamp,
        )