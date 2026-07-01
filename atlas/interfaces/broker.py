from abc import ABC, abstractmethod

from atlas.domain.order import Order
from atlas.domain.position import Position
from atlas.domain.trade import Trade


class Broker(ABC):
    """Contract for all broker adapters."""

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def place_order(self, order: Order) -> Trade:
        pass

    @abstractmethod
    def get_positions(self) -> list[Position]:
        pass