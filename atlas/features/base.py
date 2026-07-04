from abc import ABC, abstractmethod

from atlas.features.context import FeatureContext


class Feature(ABC):
    """
    Base class for every feature.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute(self, context: FeatureContext):
        pass