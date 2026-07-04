from collections.abc import Iterator

from atlas.domain.candle import Candle


class ReplayEngine:
    """
    Sequentially replays historical candles.
    """

    def __init__(self, candles: list[Candle]):
        if not candles:
            raise ValueError("Replay requires at least one candle.")

        self._candles = candles

    def __iter__(self) -> Iterator[Candle]:
        yield from self._candles