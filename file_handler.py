"""
file_handler.py
SRP: loads and saves inventory data to JSON.
Each record stores a "type" identifier so the correct subclass is rebuilt on load.
"""

import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

DEFAULT_PRODUCTS = [
    {"type": "physical", "product_id": "P001", "name": "Wireless Mouse", "price": 25.50, "stock": 2, "weight": 0.1},
    {"type": "physical", "product_id": "P002", "name": "Keyboard", "price": 45.00, "stock": 1, "weight": 0.8},
    {"type": "digital", "product_id": "P003", "name": "Antivirus Licence", "price": 39.90, "stock": 50, "download_size": 350},
]


class InventoryFileHandler:
    def __init__(self, file_path: str):
        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        return self.__file_path

    def load(self) -> Inventory:
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
                inventory.add_product(self.__create_product(record))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipping invalid record {record}: {error}")
        return inventory

    def save(self, inventory: Inventory) -> None:
        records = [self.__to_record(p) for p in inventory.get_products()]
        self.__write(records)
        print(f"Inventory successfully saved to {self.__file_path}")

    # ---------- Private helpers ----------
    @staticmethod
    def __create_product(record: dict):
        """Use the saved type identifier to rebuild the correct subclass."""
        common = (record["product_id"], record["name"], record["price"], record["stock"])
        product_type = record.get("type")

        if product_type == "physical":
            return PhysicalProduct(*common, record["weight"])
        if product_type == "digital":
            return DigitalProduct(*common, record["download_size"])
        raise ValueError(f"Unknown product type '{product_type}'")

    @staticmethod
    def __to_record(product) -> dict:
        record = {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        }
        if isinstance(product, PhysicalProduct):
            record["type"] = "physical"
            record["weight"] = product.weight
        elif isinstance(product, DigitalProduct):
            record["type"] = "digital"
            record["download_size"] = product.download_size
        else:
            raise TypeError(f"Don't know how to save {type(product).__name__}")
        return record

    def __write(self, records: list) -> None:
        folder = os.path.dirname(self.__file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.__file_path, "w") as file:
            json.dump(records, file, indent=4)
