"""
main.py
Main program: menu, user input, and calls to Inventory / Product methods.
"""

import os

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handler import InventoryFileHandler

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

failed_attempts = 0


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


def get_float(prompt: str, allow_zero: bool = True) -> float:
    global failed_attempts
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Negative values are not allowed.")
            elif value == 0 and not allow_zero:
                print("Value must be greater than 0.")
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


def get_choice(prompt: str, options: tuple) -> str:
    global failed_attempts
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(options)}.")
        failed_attempts += 1


# ---------- Menu actions ----------
def add_product(inventory) -> bool:
    global failed_attempts
    print("Product type:\n  1. Physical product\n  2. Digital product")
    product_type = get_choice("Choose type (1-2): ", ("1", "2"))

    product_id = inventory.generate_next_id()
    name = get_text("Enter product name: ")
    for existing in inventory.get_products():
        if existing.name.lower() == name.lower():
            print(f"'{existing.name}' already exists as {existing.product_id}. "
                  f"Use option 3 to update its stock.")
            return False

    price = get_float("Enter price: ")
    stock = get_int(f"Enter starting stock (0-{Product.MAX_STOCK}): ")

    try:
        if product_type == "1":
            weight = get_float("Enter weight (kg): ", allow_zero=False)
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            size = get_float("Enter download size (MB): ", allow_zero=False)
            product = DigitalProduct(product_id, name, price, stock, size)
        inventory.add_product(product)
    except ValueError as error:
        print(error)
        failed_attempts += 1
        return False

    print("\nNew Product Added:")
    product.display_information()
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
        product.update_stock(quantity)
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
        print(f"{'':<8}Fulfilment: {product.get_fulfilment_info()}")
        # Check the CAPABILITY (interface), not the specific class
        if isinstance(product, CanBeShipped):
            print(f"{'':<8}Shipping cost: ${product.calculate_shipping_cost():.2f}")


def generate_report(inventory) -> None:
    print("\n===== Session Report =====")
    print("Products in inventory:", len(inventory))
    print("Total units in stock:", inventory.total_units())
    print("Number of failed/invalid entries:", failed_attempts)


# ---------- Main loop ----------
def main():
    global failed_attempts
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
            failed_attempts += 1


if __name__ == "__main__":
    main()
