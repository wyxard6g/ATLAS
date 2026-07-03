from abc import ABC, abstractmethod

from atlas.domain.market_data import MarketData


class Feature(ABC):
    """
    Base class for every feature in ATLAS.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique feature name."""
        pass

    @abstractmethod
    def compute(self, market_data: MarketData):
        """
        Compute the feature from MarketData.
        """
        pass