"""
physical_product.py
PhysicalProduct IS-A Product (inheritance) and CAN-BE-SHIPPED (interface).
"""

from __future__ import annotations

from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING_FEE: float = 5.00
    RATE_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        if float(weight) <= 0:
            raise ValueError("Weight must be greater than 0 kg.")
        self.__weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<8}Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return f"{self.name} requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.RATE_PER_KG, 2)
