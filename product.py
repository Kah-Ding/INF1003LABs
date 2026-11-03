"""
product.py
SRP: A Product is responsible for representing and managing ONE product.
It does NOT load/save files, ask for user input, or manage other products.
"""


class Product:
    MAX_STOCK = 500  # carried over from persistent_auditor.py (inventory limit)

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        # Validate before assigning so a Product can never start in a bad state
        if not str(product_id).strip():
            raise ValueError("Product ID cannot be empty.")
        if not str(name).strip():
            raise ValueError("Product name cannot be empty.")
        if float(price) < 0:
            raise ValueError("Price cannot be negative.")
        if int(stock) < 0 or int(stock) > Product.MAX_STOCK:
            raise ValueError(f"Stock must be between 0 and {Product.MAX_STOCK}.")

        # Private attributes (name-mangled to _Product__<attr>)
        self.__product_id = str(product_id).strip().upper()
        self.__name = str(name).strip()
        self.__price = float(price)
        self.__stock = int(stock)

    # ---------- Read-only access (getters) ----------
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

    # ---------- Behaviour ----------
    def update_stock(self, quantity: int) -> None:
        """
        Change stock by `quantity` (positive = delivery, negative = removal).
        The Product decides whether the change is allowed, so outside code
        can never push the stock below 0 or above MAX_STOCK.
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
        """Tax on the value of a delivery (from calculate_tax in persistent_auditor.py)."""
        return round(abs(quantity) * self.__price * rate, 2)

    def display_information(self) -> None:
        print(f"{self.__product_id:<8}{self.__name:<20}${self.__price:>9.2f}{self.__stock:>8}")
