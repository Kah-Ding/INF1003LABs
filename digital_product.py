"""
digital_product.py
DigitalProduct IS-A Product. It does NOT implement CanBeShipped.
For LSP it keeps Product's update_stock() unchanged: stock here means
available licences/keys, so updating it has the same meaning as for Product.
"""

from __future__ import annotations

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        if float(download_size) <= 0:
            raise ValueError("Download size must be greater than 0 MB.")
        self.__download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<8}Type: Digital  | Download size: {self.__download_size:.1f} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self.name} is delivered digitally via a download link."
