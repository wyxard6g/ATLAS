from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData


class SlidingWindowBuilder:
    """
    Builds progressive MarketData windows from historical candles.
    """

    def __init__(
        self,
        candles: list[Candle],
        symbol: str,
        timeframe: str,
        source: str = "backtest",
    ):
        if not candles:
            raise ValueError("Sliding window requires at least one candle.")

        self._candles = candles
        self._symbol = symbol
        self._timeframe = timeframe
        self._source = source

    def build(self, end_index: int) -> MarketData:
        if end_index < 0 or end_index >= len(self._candles):
            raise ValueError("End index is out of range.")

        return MarketData(
            symbol=self._symbol,
            timeframe=self._timeframe,
            source=self._source,
            candles=self._candles[: end_index + 1],
        )