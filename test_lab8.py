"""
test_lab8.py
Automated checks for the Section 9 testing list.
Run with:  python -m unittest -v test_lab8
"""

from __future__ import annotations

import inspect
import os
import tempfile
import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from file_handler import InventoryFileHandler


class TestLab8(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
        self.guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, self.supplier, 3.5)
        self.software = DigitalProduct("P002", "Operating System", 199.00, 20, self.supplier, 4500)

    # ---------- Association ----------
    def test_product_stores_supplier_reference(self) -> None:
        self.assertIs(self.guitar.supplier, self.supplier)
        self.assertIs(self.software.supplier, self.supplier)

    def test_supplier_and_product_exist_independently(self) -> None:
        supplier = Supplier("S009", "Temp Supplier", "temp@example.com")
        product = PhysicalProduct("P009", "Cable", 5.0, 1, supplier, 0.2)
        del supplier
        self.assertEqual(product.supplier.name, "Temp Supplier")
        standalone = Supplier("S010", "No Products Yet", "none@example.com")
        self.assertEqual(standalone.name, "No Products Yet")

    # ---------- Aggregation ----------
    def test_product_transfers_between_inventories(self) -> None:
        inventory_a, inventory_b = Inventory(), Inventory()
        inventory_a.add_product(self.guitar)
        removed = inventory_a.remove_product("P001")
        self.assertIs(removed, self.guitar)
        self.assertIsNone(inventory_a.find_product("P001"))
        self.guitar.update_stock(1)          # still usable after removal
        inventory_b.add_product(self.guitar)
        self.assertIs(inventory_b.find_product("P001"), self.guitar)

    def test_find_product_returns_none_when_missing(self) -> None:
        self.assertIsNone(Inventory().find_product("P999"))

    # ---------- Composition ----------
    def test_order_creates_its_own_order_lines(self) -> None:
        order = Order("O001")
        order.add_order_line(self.guitar, 2)
        self.assertEqual(len(order.order_lines), 1)
        self.assertIsInstance(order.order_lines[0], OrderLine)
        with self.assertRaises(AttributeError):
            order.order_lines.append(None)  # type: ignore[attr-defined]

    def test_same_product_in_two_orders_makes_two_lines(self) -> None:
        order_1, order_2 = Order("O001"), Order("O002")
        order_1.add_order_line(self.guitar, 1)
        order_2.add_order_line(self.guitar, 1)
        self.assertIsNot(order_1.order_lines[0], order_2.order_lines[0])
        self.assertIs(order_1.order_lines[0].product, order_2.order_lines[0].product)

    def test_order_line_does_not_own_product(self) -> None:
        order = Order("O001")
        order.add_order_line(self.guitar, 1)
        order.remove_order_line("P001")
        self.assertEqual(len(order.order_lines), 0)
        self.assertEqual(self.guitar.name, "Guitar")   # product unaffected

    def test_order_total_uses_order_lines(self) -> None:
        order = Order("O001")
        order.add_order_line(self.guitar, 2)      # 700.00
        order.add_order_line(self.software, 3)    # 597.00
        self.assertEqual(order.order_lines[0].calculate_subtotal(), 700.00)
        self.assertEqual(order.calculate_total(), 1297.00)

    # ---------- Type hints ----------
    def test_type_hints_present(self) -> None:
        checks = [Product.__init__, Inventory.add_product, Inventory.remove_product,
                  Inventory.find_product, Order.add_order_line, Order.calculate_total,
                  OrderLine.calculate_subtotal, Supplier.__init__]
        for method in checks:
            hints = inspect.signature(method)
            self.assertIsNot(hints.return_annotation, inspect.Signature.empty,
                             f"{method.__qualname__} has no return type hint")
            for name, param in hints.parameters.items():
                if name != "self":
                    self.assertIsNot(param.annotation, inspect.Parameter.empty,
                                     f"{method.__qualname__}({name}) has no type hint")

    # ---------- LSP and polymorphism ----------
    def test_both_subclasses_preserve_update_stock(self) -> None:
        for product in (self.guitar, self.software):
            before = product.stock
            product.update_stock(5)
            self.assertEqual(product.stock, before + 5)
            with self.assertRaises(ValueError):
                product.update_stock(-10_000)

    def test_polymorphic_calls_through_product(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.software)
        messages = [p.get_fulfilment_info() for p in inventory.products]
        self.assertIn("physical shipping", messages[0])
        self.assertIn("digitally", messages[1])

    def test_product_is_still_abstract(self) -> None:
        with self.assertRaises(TypeError):
            Product("P999", "Generic", 1.0, 1, self.supplier)  # type: ignore[abstract]

    # ---------- Persistence ----------
    def test_json_keeps_types_and_shared_supplier(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.software)
        with tempfile.TemporaryDirectory() as folder:
            handler = InventoryFileHandler(os.path.join(folder, "inventory.json"))
            handler.save(inventory, {self.supplier.supplier_id: self.supplier})
            loaded, suppliers = handler.load()
        guitar, software = loaded.find_product("P001"), loaded.find_product("P002")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(software, DigitalProduct)
        self.assertIs(guitar.supplier, software.supplier)
        self.assertIs(guitar.supplier, suppliers["S001"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
