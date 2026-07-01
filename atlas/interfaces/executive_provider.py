from abc import ABC, abstractmethod

from atlas.domain.order import Order
from atlas.domain.trade import Trade


class ExecutionProvider(ABC):
    """Contract for execution providers."""

    @abstractmethod
    def execute_order(self, order: Order) -> Trade:
        pass