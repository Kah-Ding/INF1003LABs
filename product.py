"""
product.py
Abstract base class for every product.
- Product --> Supplier : association (Product keeps a reference, does not own it)
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    MAX_STOCK: int = 500

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        if not str(product_id).strip():
            raise ValueError("Product ID cannot be empty.")
        if not str(name).strip():
            raise ValueError("Product name cannot be empty.")
        if float(price) < 0:
            raise ValueError("Price cannot be negative.")
        if int(stock_quantity) < 0 or int(stock_quantity) > Product.MAX_STOCK:
            raise ValueError(f"Stock must be between 0 and {Product.MAX_STOCK}.")
        if not isinstance(supplier, Supplier):
            raise TypeError("supplier must be a Supplier object.")

        self.__product_id: str = str(product_id).strip().upper()
        self.__name: str = str(name).strip()
        self.__price: float = float(price)
        self.__stock: int = int(stock_quantity)
        self.__supplier: Supplier = supplier   # association: a reference, not ownership

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

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ---------- Concrete (shared) behaviour ----------
    def update_stock(self, quantity: int) -> None:
        """
        Contract every subclass must keep (LSP):
        add `quantity` to stock (negative removes); raise ValueError if the
        result would be below 0 or above MAX_STOCK; return nothing.
        """
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
        print(f"{self.__product_id:<8}{self.__name:<20}${self.__price:>9.2f}{self.__stock:>8}"
              f"   Supplier: {self.__supplier.name}")

    # ---------- Abstract behaviour ----------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Describe how this product is delivered to the customer."""
        pass
