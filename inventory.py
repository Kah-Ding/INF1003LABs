"""
inventory.py
Inventory o-- Product is AGGREGATION:
the Inventory holds references to Products but does not create them or control
their lifecycle. Removing a Product only removes the reference.
"""

from __future__ import annotations

from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []   # typed with the BASE class

    @property
    def products(self) -> list[Product]:
        """A copy, so outside code can loop over products but not edit the list."""
        return list(self.__products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.find_product(product.product_id) is not None:
            raise ValueError(f"Product ID {product.product_id} already exists in this inventory.")
        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the reference and hand the (still existing) Product back to the caller."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, keyword: str) -> list[Product]:
        keyword = keyword.strip().lower()
        return [
            p for p in self.__products
            if keyword in p.product_id.lower() or keyword in p.name.lower()
        ]

    def display_all_products(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return
        print(f"{'ID':<8}{'Name':<20}{'Price':>10}{'Stock':>8}")
        print("-" * 70)
        for product in self.__products:
            product.display_information()   # polymorphism: each object picks its own version

    def generate_next_id(self) -> str:
        highest = 0
        for product in self.__products:
            digits = "".join(ch for ch in product.product_id if ch.isdigit())
            if digits:
                highest = max(highest, int(digits))
        return f"P{highest + 1:03d}"

    def total_units(self) -> int:
        return sum(p.stock for p in self.__products)

    def __len__(self) -> int:
        return len(self.__products)
