"""
order.py
Order *-- OrderLine is COMPOSITION:
the Order creates its own OrderLines, they belong to exactly one Order,
are never passed in from outside, and disappear with the Order.
"""

from __future__ import annotations

from product import Product
from order_line import OrderLine


class Order:
    def __init__(self, order_id: str) -> None:
        if not order_id.strip():
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id.strip().upper()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        """Read-only view: lines can be looked at, but not added/moved from outside."""
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """The Order CREATES the OrderLine itself - nobody else does."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        product_id = product_id.strip().upper()
        for line in self.__order_lines:
            if line.product.product_id == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return round(sum(line.calculate_subtotal() for line in self.__order_lines), 2)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
            return
        for line in self.__order_lines:
            line.display_information()
        print(f"  {'Total:':>45} ${self.calculate_total():>9.2f}")
