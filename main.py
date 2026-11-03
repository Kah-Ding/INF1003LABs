"""
main.py
Main program: displays the menu, gets user input, and calls Inventory/Product methods.
It never touches a Product's private data directly.
"""

import os

from product import Product
from file_handler import InventoryFileHandler

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

failed_attempts = 0  # tracked like `failed` in persistent_auditor.py


# ---------- Input helpers ----------
def get_int(prompt: str, allow_negative: bool = False) -> int:
    global failed_attempts
    while True:
        raw = input(prompt).strip()
        digits = raw[1:] if raw.startswith("-") else raw
        if digits.isdigit():
            if raw.startswith("-") and not allow_negative:
                print("Negative values are not allowed.")
                failed_attempts += 1
                continue
            return int(raw)
        print("Invalid input. Please enter a whole number.")
        failed_attempts += 1


def get_price(prompt: str) -> float:
    global failed_attempts
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Negative values are not allowed.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        failed_attempts += 1


def get_text(prompt: str) -> str:
    global failed_attempts
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Input cannot be empty.")
        failed_attempts += 1


# ---------- Menu actions ----------
def add_product(inventory) -> bool:
    global failed_attempts
    product_id = inventory.generate_next_id()
    name = get_text("Enter product name: ")

    for existing in inventory.get_products():
        if existing.name.lower() == name.lower():
            print(f"'{existing.name}' already exists as {existing.product_id}. "
                  f"Use option 3 to update its stock.")
            return False

    price = get_price("Enter price: ")
    stock = get_int(f"Enter starting stock (0-{Product.MAX_STOCK}): ")
    try:
        inventory.add_product(Product(product_id, name, price, stock))
    except ValueError as error:
        print(error)
        failed_attempts += 1
        return False
    print(f"\nNew Product Added: {product_id}, {name}, ${price:.2f}, {stock}")
    return True


def update_stock(inventory) -> bool:
    global failed_attempts
    product = inventory.find_by_id(get_text("Enter product ID: "))
    if product is None:
        print("Product not found.")
        failed_attempts += 1
        return False

    print(f"{product.name} currently has {product.stock} units.")
    quantity = get_int("Enter quantity to add (use a negative number to remove): ",
                       allow_negative=True)
    try:
        product.update_stock(quantity)  # Product validates its own state
    except ValueError as error:
        print(error)
        failed_attempts += 1
        return False

    print(f"Stock updated. {product.name} now has {product.stock} units.")
    if quantity > 0:
        print(f"Tax amount for this delivery: ${product.calculate_tax(quantity):.2f}")
    return True


def search_product(inventory) -> None:
    results = inventory.search_product(get_text("Enter product ID or name to search: "))
    if not results:
        print("No matching products found.")
        return
    print(f"{'ID':<8}{'Name':<20}{'Price':>10}{'Stock':>8}")
    print("-" * 46)
    for product in results:
        product.display_information()


def generate_report(inventory) -> None:
    print("\n===== Session Report =====")
    print("Products in inventory:", len(inventory))
    print("Total units in stock:", inventory.total_units())
    print("Number of failed/invalid entries:", failed_attempts)


# ---------- Main loop ----------
def main():
    file_handler = InventoryFileHandler(INVENTORY_FILE)
    inventory = file_handler.load()
    unsaved_changes = False

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()
        print()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            unsaved_changes = add_product(inventory) or unsaved_changes
        elif choice == "3":
            unsaved_changes = update_stock(inventory) or unsaved_changes
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            file_handler.save(inventory)
            unsaved_changes = False
        elif choice == "6":
            if unsaved_changes:
                if input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower() == "y":
                    file_handler.save(inventory)
            generate_report(inventory)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")
            global failed_attempts
            failed_attempts += 1


if __name__ == "__main__":
    main()
