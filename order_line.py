"""
order_line.py
One product + quantity inside an Order.
- OrderLine --> Product : association (refers to the Product, does not own it)
- Only an Order should create OrderLines (Order *-- OrderLine is composition).
"""

from __future__ import annotations

from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if int(quantity) <= 0:
            raise ValueError("Order quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = int(quantity)

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return round(self.__product.price * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"  {self.__product.product_id:<8}{self.__product.name:<20}"
              f"{self.__quantity:>4} x ${self.__product.price:>8.2f} = ${self.calculate_subtotal():>9.2f}")
