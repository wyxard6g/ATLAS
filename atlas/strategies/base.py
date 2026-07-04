from abc import ABC, abstractmethod

from atlas.domain.feature_set import FeatureSet
from atlas.domain.signal import Signal


class Strategy(ABC):
    """
    Base class for every trading strategy.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate(self, feature_set: FeatureSet) -> Signal:
        """
        Generate a trading signal from computed features.
        """
        pass