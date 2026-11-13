"""
supplier.py
SRP: represents one supplier.
Supplier ---- Product is an ASSOCIATION: neither owns the other, both exist independently.
"""

from __future__ import annotations


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if "@" not in contact_email or "." not in contact_email.split("@")[-1]:
            raise ValueError("Please enter a valid email address.")
        self.__supplier_id: str = supplier_id.strip().upper()
        self.__name: str = name.strip()
        self.__contact_email: str = contact_email.strip()

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"{self.__supplier_id:<8}{self.__name:<24}{self.__contact_email}")
