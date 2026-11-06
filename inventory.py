"""
inventory.py
SRP: manages a COLLECTION of Product objects.
Unchanged in logic from Lab 6 - it works with any Product subclass (OCP in action).
"""

from product import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.find_by_id(product.product_id) is not None:
            raise ValueError(f"Product ID {product.product_id} already exists.")
        self.__products.append(product)

    def find_by_id(self, product_id: str):
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, keyword: str) -> list:
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
            product.display_information()   # each subclass displays itself

    def get_products(self) -> list:
        return list(self.__products)

    def generate_next_id(self) -> str:
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
