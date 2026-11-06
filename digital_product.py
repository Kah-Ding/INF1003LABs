"""
digital_product.py
A DigitalProduct IS-A Product. It does NOT implement CanBeShipped.
"""

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        if float(download_size) <= 0:
            raise ValueError("Download size must be greater than 0 MB.")
        self.__download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<8}Type: Digital  | Download size: {self.__download_size:.1f} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self.name} is delivered digitally via a download link."
