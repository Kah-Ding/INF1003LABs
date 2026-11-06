"""
product.py
Abstract base class for every product.
SRP: represent and manage the data/behaviour COMMON to all products.
OCP: new product types extend this class instead of modifying it.
"""

from abc import ABC, abstractmethod


class Product(ABC):
    MAX_STOCK = 500

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if not str(product_id).strip():
            raise ValueError("Product ID cannot be empty.")
        if not str(name).strip():
            raise ValueError("Product name cannot be empty.")
        if float(price) < 0:
            raise ValueError("Price cannot be negative.")
        if int(stock) < 0 or int(stock) > Product.MAX_STOCK:
            raise ValueError(f"Stock must be between 0 and {Product.MAX_STOCK}.")

        self.__product_id = str(product_id).strip().upper()
        self.__name = str(name).strip()
        self.__price = float(price)
        self.__stock = int(stock)

    # ---------- Read-only access ----------
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    # ---------- Concrete (shared) behaviour ----------
    def update_stock(self, quantity: int) -> None:
        new_stock = self.__stock + int(quantity)
        if new_stock < 0:
            raise ValueError(
                f"Not enough stock. {self.__name} only has {self.__stock} units."
            )
        if new_stock > Product.MAX_STOCK:
            raise ValueError(
                f"Inventory limit exceeded! Stock cannot exceed "
                f"{Product.MAX_STOCK} units (would be {new_stock})."
            )
        self.__stock = new_stock

    def calculate_tax(self, quantity: int, rate: float = 0.10) -> float:
        return round(abs(quantity) * self.__price * rate, 2)

    def display_information(self) -> None:
        """Common information. Subclasses call this via super() and add their own."""
        print(f"{self.__product_id:<8}{self.__name:<20}${self.__price:>9.2f}{self.__stock:>8}")

    # ---------- Abstract behaviour (subclasses MUST implement) ----------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Describe how this product is delivered to the customer."""
        pass
