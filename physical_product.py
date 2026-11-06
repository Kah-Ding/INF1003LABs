"""
physical_product.py
A PhysicalProduct IS-A Product, and it CAN-BE-SHIPPED.
Single class inheritance (Product) + one interface (CanBeShipped).
"""

from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING_FEE = 5.00   # flat fee per shipment
    RATE_PER_KG = 2.00         # extra cost per kg

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)   # reuse Product's constructor
        if float(weight) <= 0:
            raise ValueError("Weight must be greater than 0 kg.")
        self.__weight = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    # Overrides Product.display_information, reusing the parent's output
    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<8}Type: Physical | Weight: {self.__weight:.2f} kg")

    # Implements Product's abstract method
    def get_fulfilment_info(self) -> str:
        return f"{self.name} requires physical shipping."

    # Implements CanBeShipped's abstract method
    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING_FEE + self.__weight * self.RATE_PER_KG, 2)
