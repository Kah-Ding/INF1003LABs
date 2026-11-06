"""
test_lab7.py
Automated checks for the Section 7 testing list.
Run with:  python -m unittest -v test_lab7
"""

import os
import tempfile
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import InventoryFileHandler


class TestLab7(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, 3.5)
        self.os_licence = DigitalProduct("P002", "Operating System", 199.00, 20, 4500)

    def test_physical_stores_weight(self):
        self.assertEqual(self.guitar.weight, 3.5)

    def test_digital_stores_download_size(self):
        self.assertEqual(self.os_licence.download_size, 4500)

    def test_both_implement_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os_licence.get_fulfilment_info())

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P999", "Generic", 1.0, 1)

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P010", "Cable", 5.0, 1, 0.5)
        heavy = PhysicalProduct("P011", "Amplifier", 500.0, 1, 20)
        self.assertEqual(light.calculate_shipping_cost(), 6.00)    # 5 + 0.5*2
        self.assertEqual(heavy.calculate_shipping_cost(), 45.00)   # 5 + 20*2

    def test_digital_is_not_shippable(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertNotIsInstance(self.os_licence, CanBeShipped)
        self.assertFalse(hasattr(self.os_licence, "calculate_shipping_cost"))

    def test_inventory_operations(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.os_licence)
        self.assertEqual(len(inventory), 2)
        self.assertEqual(inventory.search_product("gui"), [self.guitar])
        self.assertEqual(inventory.generate_next_id(), "P003")
        self.guitar.update_stock(10)
        self.assertEqual(inventory.find_by_id("p001").stock, 15)
        with self.assertRaises(ValueError):
            self.guitar.update_stock(-100)

    def test_json_preserves_types(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.os_licence)
        with tempfile.TemporaryDirectory() as folder:
            handler = InventoryFileHandler(os.path.join(folder, "inventory.json"))
            handler.save(inventory)
            reloaded = handler.load()
        guitar = reloaded.find_by_id("P001")
        os_licence = reloaded.find_by_id("P002")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(os_licence, DigitalProduct)
        self.assertEqual(guitar.weight, 3.5)
        self.assertEqual(os_licence.download_size, 4500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
