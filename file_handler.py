"""
file_handler.py
SRP: Responsible ONLY for loading and saving inventory data to JSON.
"""

import json
import os

from product import Product
from inventory import Inventory

DEFAULT_PRODUCTS = [
    {"product_id": "P001", "name": "Wireless Mouse", "price": 25.50, "stock": 2},
    {"product_id": "P002", "name": "Keyboard", "price": 45.00, "stock": 1},
    {"product_id": "P003", "name": "USB Cable", "price": 9.90, "stock": 3},
]


class InventoryFileHandler:
    def __init__(self, file_path: str):
        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        return self.__file_path

    def load(self) -> Inventory:
        """Build an Inventory from the JSON file. Seeds defaults if missing/empty."""
        inventory = Inventory()

        if not os.path.exists(self.__file_path) or os.path.getsize(self.__file_path) == 0:
            print(f"No saved inventory found. Creating {self.__file_path} with default products.")
            records = DEFAULT_PRODUCTS
            self.__write(records)
        else:
            try:
                with open(self.__file_path, "r") as file:
                    records = json.load(file)
            except json.JSONDecodeError:
                print("Warning: inventory file is corrupted. Starting with an empty inventory.")
                return inventory

        for record in records:
            try:
                inventory.add_product(Product(
                    record["product_id"], record["name"], record["price"], record["stock"]
                ))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipping invalid record {record}: {error}")
        return inventory

    def save(self, inventory: Inventory) -> None:
        records = [
            {"product_id": p.product_id, "name": p.name, "price": p.price, "stock": p.stock}
            for p in inventory.get_products()
        ]
        self.__write(records)
        print(f"Inventory successfully saved to {self.__file_path}")

    def __write(self, records: list) -> None:
        folder = os.path.dirname(self.__file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.__file_path, "w") as file:
            json.dump(records, file, indent=4)
