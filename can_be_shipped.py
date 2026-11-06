"""
can_be_shipped.py
Interface-style ABC: a contract for any object that "must be able to" be shipped.
No attributes and no implementation - only the required behaviour.
"""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the cost of shipping this item."""
        pass
