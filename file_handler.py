"""
file_handler.py
SRP: loads and saves suppliers and products to JSON.

File layout:
{
  "suppliers": [ {supplier_id, name, contact_email}, ... ],
  "products":  [ {type, product_id, name, price, stock, supplier_id, weight | download_size}, ... ]
}
Products store the supplier's ID; on load they are re-linked to the SAME Supplier object,
so several products share one supplier (association), just like before saving.
"""

from __future__ import annotations

import json
import os

from supplier import Supplier
from product import Product
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

DEFAULT_DATA: dict[str, list[dict]] = {
    "suppliers": [
        {"supplier_id": "S001", "name": "TechSource Pte Ltd", "contact_email": "sales@techsource.sg"},
        {"supplier_id": "S002", "name": "SoftLicence Asia", "contact_email": "orders@softlicence.asia"},
    ],
    "products": [
        {"type": "physical", "product_id": "P001", "name": "Wireless Mouse", "price": 25.50,
         "stock": 20, "supplier_id": "S001", "weight": 0.1},
        {"type": "physical", "product_id": "P002", "name": "Keyboard", "price": 45.00,
         "stock": 10, "supplier_id": "S001", "weight": 0.8},
        {"type": "digital", "product_id": "P003", "name": "Antivirus Licence", "price": 39.90,
         "stock": 50, "supplier_id": "S002", "download_size": 350},
    ],
}

UNKNOWN_SUPPLIER: dict[str, str] = {
    "supplier_id": "S000", "name": "Unknown Supplier", "contact_email": "unknown@example.com"
}


class InventoryFileHandler:
    def __init__(self, file_path: str) -> None:
        self.__file_path: str = file_path

    @property
    def file_path(self) -> str:
        return self.__file_path

    def load(self) -> tuple[Inventory, dict[str, Supplier]]:
        inventory = Inventory()
        suppliers: dict[str, Supplier] = {}

        if not os.path.exists(self.__file_path) or os.path.getsize(self.__file_path) == 0:
            print(f"No saved inventory found. Creating {self.__file_path} with sample data.")
            data = DEFAULT_DATA
            self.__write(data)
        else:
            try:
                with open(self.__file_path, "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                print("Warning: inventory file is corrupted. Starting with an empty inventory.")
                return inventory, suppliers

        # Lab 7 files were a plain list of products with no suppliers
        if isinstance(data, list):
            print("Old (Lab 7) file format found - products assigned to 'Unknown Supplier'.")
            data = {"suppliers": [UNKNOWN_SUPPLIER],
                    "products": [{**p, "supplier_id": "S000"} for p in data]}

        for record in data.get("suppliers", []):
            try:
                supplier = Supplier(record["supplier_id"], record["name"], record["contact_email"])
                suppliers[supplier.supplier_id] = supplier
            except (KeyError, ValueError) as error:
                print(f"Skipping invalid supplier {record}: {error}")

        for record in data.get("products", []):
            try:
                supplier = suppliers[record["supplier_id"]]
                inventory.add_product(self.__create_product(record, supplier))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipping invalid product {record}: {error}")

        return inventory, suppliers

    def save(self, inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
        data = {
            "suppliers": [
                {"supplier_id": s.supplier_id, "name": s.name, "contact_email": s.contact_email}
                for s in suppliers.values()
            ],
            "products": [self.__to_record(p) for p in inventory.products],
        }
        self.__write(data)
        print(f"Inventory successfully saved to {self.__file_path}")

    # ---------- Private helpers ----------
    @staticmethod
    def __create_product(record: dict, supplier: Supplier) -> Product:
        common = (record["product_id"], record["name"], record["price"], record["stock"], supplier)
        product_type = record.get("type")
        if product_type == "physical":
            return PhysicalProduct(*common, record["weight"])
        if product_type == "digital":
            return DigitalProduct(*common, record["download_size"])
        raise ValueError(f"Unknown product type '{product_type}'")

    @staticmethod
    def __to_record(product: Product) -> dict:
        record: dict = {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "supplier_id": product.supplier.supplier_id,
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

    def __write(self, data: dict) -> None:
        folder = os.path.dirname(self.__file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.__file_path, "w") as file:
            json.dump(data, file, indent=4)
