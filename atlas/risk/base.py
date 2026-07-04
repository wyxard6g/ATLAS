from abc import ABC, abstractmethod

from atlas.domain.signal import Signal


class RiskModel(ABC):
    """
    Base class for every risk model.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def approve(self, signal: Signal) -> bool:
        """
        Return True if the signal passes risk validation.
        """
        pass