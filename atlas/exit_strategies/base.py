from abc import ABC, abstractmethod

from atlas.domain.position import Position


class ExitStrategy(ABC):
    """
    Base class for exit strategies.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def should_exit(
        self,
        position: Position,
        current_price: float,
    ) -> bool:
        pass