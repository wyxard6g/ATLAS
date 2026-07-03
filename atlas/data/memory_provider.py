from datetime import datetime

from atlas.data.validators import validate_candles
from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.domain.tick import Tick
from atlas.interfaces.data_provider import DataProvider


class MemoryDataProvider(DataProvider):
    """
    In-memory market data provider for testing and development.
    """

    def __init__(
        self,
        candles: list[Candle],
        symbol: str,
        timeframe: str,
        source: str = "memory",
    ):
        validate_candles(candles)

        self._candles = candles
        self._symbol = symbol
        self._timeframe = timeframe
        self._source = source

    def get_market_data(
        self,
        start: datetime,
        end: datetime,
    ) -> MarketData:
        candles = [
            candle
            for candle in self._candles
            if start <= candle.timestamp <= end
        ]

        return MarketData(
            symbol=self._symbol,
            timeframe=self._timeframe,
            source=self._source,
            candles=candles,
        )

    def get_latest_tick(self, symbol: str) -> Tick:
        latest = self._candles[-1]

        return Tick(
            symbol=symbol,
            price=latest.close,
            volume=latest.volume,
            timestamp=latest.timestamp,
        )