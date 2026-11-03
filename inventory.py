"""
inventory.py
SRP: An Inventory is responsible for managing a COLLECTION of Product objects.
"""

from product import Product


class Inventory:
    def __init__(self):
        self.__products = []  # list of Product objects

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.find_by_id(product.product_id) is not None:
            raise ValueError(f"Product ID {product.product_id} already exists.")
        self.__products.append(product)

    def find_by_id(self, product_id: str):
        """Return the Product with an exact ID match, or None."""
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, keyword: str) -> list:
        """Return all products whose ID or name contains the keyword (case-insensitive)."""
        keyword = keyword.strip().lower()
        return [
            p for p in self.__products
            if keyword in p.product_id.lower() or keyword in p.name.lower()
        ]

    def display_all(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return
        print(f"{'ID':<8}{'Name':<20}{'Price':>10}{'Stock':>8}")
        print("-" * 46)
        for product in self.__products:
            product.display_information()

    def get_products(self) -> list:
        """Return a copy so outside code can't modify the internal list directly."""
        return list(self.__products)

    def generate_next_id(self) -> str:
        """Next ID after the highest existing one (like order_id + 1 in persistent_auditor.py)."""
        highest = 0
        for product in self.__products:
            digits = "".join(ch for ch in product.product_id if ch.isdigit())
            if digits:
                highest = max(highest, int(digits))
        return f"P{highest + 1:03d}"

    def total_units(self) -> int:
        return sum(p.stock for p in self.__products)

    def __len__(self):
        return len(self.__products)
