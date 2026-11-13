"""
main.py
Main program: menu, user input, and calls to Inventory / Product / Order methods.
"""

from __future__ import annotations

import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from file_handler import InventoryFileHandler

INVENTORY_FILE: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

failed_attempts: int = 0


# ---------- Input helpers ----------
def record_failure(message: str) -> None:
    global failed_attempts
    print(message)
    failed_attempts += 1


def get_int(prompt: str, allow_negative: bool = False) -> int:
    while True:
        raw = input(prompt).strip()
        digits = raw[1:] if raw.startswith("-") else raw
        if digits.isdigit():
            if raw.startswith("-") and not allow_negative:
                record_failure("Negative values are not allowed.")
                continue
            return int(raw)
        record_failure("Invalid input. Please enter a whole number.")


def get_float(prompt: str, allow_zero: bool = True) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            record_failure("Invalid input. Please enter a numeric value.")
            continue
        if value < 0:
            record_failure("Negative values are not allowed.")
        elif value == 0 and not allow_zero:
            record_failure("Value must be greater than 0.")
        else:
            return value


def get_text(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text
        record_failure("Input cannot be empty.")


def get_choice(prompt: str, options: tuple[str, ...]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        record_failure(f"Invalid choice. Please enter one of: {', '.join(options)}.")


# ---------- Supplier actions ----------
def display_suppliers(suppliers: dict[str, Supplier]) -> None:
    if not suppliers:
        print("No suppliers yet.")
        return
    print(f"{'ID':<8}{'Name':<24}Email")
    print("-" * 60)
    for supplier in suppliers.values():
        supplier.display_information()


def add_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    supplier_id = f"S{len(suppliers) + 1:03d}"
    while supplier_id in suppliers:
        supplier_id = f"S{int(supplier_id[1:]) + 1:03d}"
    name = get_text("Enter supplier name: ")
    email = get_text("Enter supplier contact email: ")
    try:
        supplier = Supplier(supplier_id, name, email)
    except ValueError as error:
        record_failure(str(error))
        return None
    suppliers[supplier.supplier_id] = supplier
    print(f"Supplier {supplier.supplier_id} added.")
    return supplier


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    display_suppliers(suppliers)
    while True:
        answer = get_text("Enter supplier ID (or 'new' to add a supplier): ")
        if answer.lower() == "new":
            return add_supplier(suppliers)
        supplier = suppliers.get(answer.upper())
        if supplier is not None:
            return supplier
        record_failure("Supplier not found.")


def manage_suppliers(suppliers: dict[str, Supplier]) -> bool:
    print("  1. View suppliers\n  2. Add a supplier")
    if get_choice("Choose (1-2): ", ("1", "2")) == "1":
        display_suppliers(suppliers)
        return False
    return add_supplier(suppliers) is not None


# ---------- Product actions ----------
def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    print("Product type:\n  1. Physical product\n  2. Digital product")
    product_type = get_choice("Choose type (1-2): ", ("1", "2"))

    product_id = inventory.generate_next_id()
    name = get_text("Enter product name: ")
    for existing in inventory.products:
        if existing.name.lower() == name.lower():
            print(f"'{existing.name}' already exists as {existing.product_id}. "
                  f"Use option 3 to update its stock.")
            return False

    price = get_float("Enter price: ")
    stock = get_int(f"Enter starting stock (0-{Product.MAX_STOCK}): ")
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return False

    product: Product
    try:
        if product_type == "1":
            weight = get_float("Enter weight (kg): ", allow_zero=False)
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            size = get_float("Enter download size (MB): ", allow_zero=False)
            product = DigitalProduct(product_id, name, price, stock, supplier, size)
        inventory.add_product(product)
    except ValueError as error:
        record_failure(str(error))
        return False

    print("\nNew Product Added:")
    product.display_information()
    return True


def update_stock(inventory: Inventory) -> bool:
    product = inventory.find_product(get_text("Enter product ID: "))
    if product is None:
        record_failure("Product not found.")
        return False

    print(f"{product.name} currently has {product.stock} units.")
    quantity = get_int("Enter quantity to add (use a negative number to remove): ",
                       allow_negative=True)
    try:
        product.update_stock(quantity)
    except ValueError as error:
        record_failure(str(error))
        return False

    print(f"Stock updated. {product.name} now has {product.stock} units.")
    if quantity > 0:
        print(f"Tax amount for this delivery: ${product.calculate_tax(quantity):.2f}")
    return True


def show_product_details(product: Product) -> None:
    """Works for ANY Product subclass (LSP + polymorphism)."""
    product.display_information()
    print(f"{'':<8}Fulfilment: {product.get_fulfilment_info()}")
    print(f"{'':<8}Supplier contact: {product.supplier.contact_email}")


def search_product(inventory: Inventory) -> None:
    results = inventory.search_product(get_text("Enter product ID or name to search: "))
    if not results:
        print("No matching products found.")
        return
    for product in results:
        show_product_details(product)
        # Optional capability check (interface), not a choice between subclass methods
        if isinstance(product, CanBeShipped):
            print(f"{'':<8}Shipping cost: ${product.calculate_shipping_cost():.2f}")


def remove_product(inventory: Inventory) -> bool:
    removed = inventory.remove_product(get_text("Enter product ID to remove: "))
    if removed is None:
        record_failure("Product not found.")
        return False
    # Aggregation: only the reference is removed - the object itself still exists
    print(f"{removed.name} ({removed.product_id}) removed from the inventory.")
    return True


# ---------- Order actions ----------
def create_order(inventory: Inventory, orders: list[Order]) -> bool:
    order = Order(f"O{len(orders) + 1:03d}")
    print(f"Creating order {order.order_id}. Leave the product ID blank to finish.")

    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            record_failure("Product not found.")
            continue
        if any(line.product is product for line in order.order_lines):
            record_failure(f"{product.name} is already in this order.")
            continue
        quantity = get_int(f"Quantity of {product.name} (in stock: {product.stock}): ")
        if quantity == 0 or quantity > product.stock:
            record_failure("Quantity must be between 1 and the available stock.")
            continue
        order.add_order_line(product, quantity)   # the Order creates the OrderLine itself

    if not order.order_lines:
        print("Order cancelled - no items added.")
        return False

    print()
    order.display_information()
    if input("Confirm order? (y/n): ").strip().lower() != "y":
        # Composition: discarding the Order discards its OrderLines with it
        print("Order cancelled. Its order lines were discarded with it.")
        return False

    for line in order.order_lines:
        line.product.update_stock(-line.quantity)
    orders.append(order)
    print(f"Order {order.order_id} confirmed. Stock updated.")
    return True


def view_orders(orders: list[Order]) -> None:
    if not orders:
        print("No orders placed this session.")
        return
    for order in orders:
        order.display_information()
        print()


def generate_report(inventory: Inventory, orders: list[Order]) -> None:
    print("\n===== Session Report =====")
    print("Products in inventory:", len(inventory))
    print("Total units in stock:", inventory.total_units())
    print("Orders placed:", len(orders))
    print(f"Order revenue: ${sum(o.calculate_total() for o in orders):.2f}")
    print("Number of failed/invalid entries:", failed_attempts)


# ---------- Main loop ----------
def main() -> None:
    file_handler = InventoryFileHandler(INVENTORY_FILE)
    inventory, suppliers = file_handler.load()
    orders: list[Order] = []
    unsaved_changes = False

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Remove a product")
        print("6. Suppliers")
        print("7. Create an order")
        print("8. View orders")
        print("9. Save inventory")
        print("0. Exit")
        choice = input("Enter your choice (0-9): ").strip()
        print()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            unsaved_changes = add_product(inventory, suppliers) or unsaved_changes
        elif choice == "3":
            unsaved_changes = update_stock(inventory) or unsaved_changes
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            unsaved_changes = remove_product(inventory) or unsaved_changes
        elif choice == "6":
            unsaved_changes = manage_suppliers(suppliers) or unsaved_changes
        elif choice == "7":
            unsaved_changes = create_order(inventory, orders) or unsaved_changes
        elif choice == "8":
            view_orders(orders)
        elif choice == "9":
            file_handler.save(inventory, suppliers)
            unsaved_changes = False
        elif choice == "0":
            if unsaved_changes:
                if input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower() == "y":
                    file_handler.save(inventory, suppliers)
            generate_report(inventory, orders)
            print("Goodbye!")
            break
        else:
            record_failure("Invalid choice. Please enter a number from 0 to 9.")


if __name__ == "__main__":
    main()
