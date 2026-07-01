from abc import ABC, abstractmethod

from atlas.domain.order import Order
from atlas.domain.signal import Signal


class RiskModel(ABC):
    """Contract for risk models."""

    @abstractmethod
    def approve_signal(self, signal: Signal) -> bool:
        pass

    @abstractmethod
    def validate_order(self, order: Order) -> bool:
        pass