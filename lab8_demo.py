"""
lab8_demo.py
Runs each lab scenario step by step and prints the result.
Use the output as evidence for your "Predict first" notes and screenshots.
Run with:  python lab8_demo.py
"""

from __future__ import annotations

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


def show_product_details(product: Product) -> None:
    """Section 6.2: accepts ANY Product - no subclass checks."""
    product.display_information()
    print(f"{'':<8}{product.get_fulfilment_info()}")


def section_2_association() -> None:
    heading("Section 2 - Association: Supplier and Product")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, supplier, 3.5)
    os_licence = DigitalProduct("P002", "Operating System", 199.00, 20, supplier, 4500)

    print("Supplier info through each product:")
    print(f"  {guitar.name} -> {guitar.supplier.name} ({guitar.supplier.contact_email})")
    print(f"  {os_licence.name} -> {os_licence.supplier.name} ({os_licence.supplier.contact_email})")
    print(f"Both products share the same Supplier object: {guitar.supplier is os_licence.supplier}")
    print(f"Supplier and Product are separate objects:     {guitar.supplier is not guitar}")

    print("\nPredict first: running `del supplier` ...")
    del supplier
    print("After del, guitar.supplier.name =", guitar.supplier.name)
    print("-> `del` only removes the variable NAME. The Supplier object stays alive because")
    print("   the products still hold references to it.")


def section_3_aggregation() -> None:
    heading("Section 3 - Aggregation: Inventory and Product")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    mouse = PhysicalProduct("P010", "Wireless Mouse", 25.50, 20, supplier, 0.1)
    print("1. Product created BEFORE any inventory exists:", mouse.name)

    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(mouse)
    print("2. Added to Inventory A. A has", len(inventory_a), "product(s).")

    removed = inventory_a.remove_product("P010")
    print("3. Removed from Inventory A. A has", len(inventory_a), "product(s).")
    print("   Predict first: does the product still work?")
    mouse.update_stock(5)
    print(f"   Yes - update_stock(5) worked, stock is now {mouse.stock}.")
    print(f"   remove_product() returned the same object: {removed is mouse}")

    inventory_b.add_product(mouse)
    print("4. Same object added to Inventory B:", inventory_b.find_product("P010") is mouse)

    inventory_b.remove_product("P010")
    print("5. Inventory B emptied. Product still exists:", mouse.name, "- stock", mouse.stock)


def section_4_composition() -> None:
    heading("Section 4 - Composition: Order and OrderLine")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    keyboard = PhysicalProduct("P020", "Keyboard", 45.00, 10, supplier, 0.8)
    antivirus = DigitalProduct("P021", "Antivirus Licence", 39.90, 50, supplier, 350)

    order_1 = Order("O001")
    order_1.add_order_line(keyboard, 2)
    order_1.add_order_line(antivirus, 3)
    order_1.display_information()

    print("\nPredict first: same Product added to a second Order ...")
    order_2 = Order("O002")
    order_2.add_order_line(keyboard, 1)
    line_1 = order_1.order_lines[0]
    line_2 = order_2.order_lines[0]
    print(f"OrderLine objects are different: line_1 is line_2 -> {line_1 is line_2}")
    print(f"  id(line_1) = {id(line_1)}\n  id(line_2) = {id(line_2)}")
    print(f"Both lines point to ONE Product:  line_1.product is line_2.product -> "
          f"{line_1.product is line_2.product}")
    print("-> 2 OrderLine objects, 1 Product object.")

    print("\nRemoving the keyboard line from Order O001 through an Order method:")
    order_1.remove_order_line("P020")
    order_1.display_information()
    print(f"The keyboard Product still exists (stock {keyboard.stock}) - only the line was removed.")

    print("\nOrder lines can only be read from outside, not appended to:")
    try:
        order_1.order_lines.append(line_2)  # type: ignore[attr-defined]
    except AttributeError as error:
        print(f"  order_1.order_lines.append(...) -> AttributeError: {error}")


def section_6_lsp() -> None:
    heading("Section 6 - Liskov Substitution: show_product_details(product: Product)")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    products: list[Product] = [
        PhysicalProduct("P030", "Monitor", 299.99, 8, supplier, 4.2),
        DigitalProduct("P031", "Photo Editor", 129.00, 40, supplier, 2048),
    ]
    for product in products:
        show_product_details(product)

    print("\nShared expectation: update_stock() adds to stock and rejects going below 0.")
    for product in products:
        before = product.stock
        product.update_stock(5)
        try:
            product.update_stock(-1000)
        except ValueError:
            result = "rejected -1000 with ValueError"
        print(f"  {type(product).__name__:<16}{before} + 5 = {product.stock}, {result}")


def section_7_polymorphism() -> None:
    heading("Section 7 - Polymorphism through the Product collection")
    supplier = Supplier("S002", "SoftLicence Asia", "orders@softlicence.asia")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P040", "Speaker", 89.00, 12, supplier, 1.6))
    inventory.add_product(DigitalProduct("P041", "Music Software", 59.00, 30, supplier, 900))

    print("Predict first: what will get_fulfilment_info() print for each product?\n")
    for product in inventory.products:   # one loop, no isinstance()
        product.display_information()
        print(f"{'':<8}{product.get_fulfilment_info()}")


if __name__ == "__main__":
    section_2_association()
    section_3_aggregation()
    section_4_composition()
    section_6_lsp()
    section_7_polymorphism()
