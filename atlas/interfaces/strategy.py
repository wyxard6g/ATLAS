from abc import ABC, abstractmethod

from atlas.domain.candle import Candle
from atlas.domain.signal import Signal


class Strategy(ABC):
    """Contract for all trading strategies."""

    @abstractmethod
    def generate_signal(self, candles: list[Candle]) -> Signal:
        pass