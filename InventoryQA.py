import unittest
import threading
from InventoryManagement import InventorySystem

class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.system = InventorySystem()
        self.system.add_supplier("S1", "Global Logistics Corp")
        self.system.add_product("P100", "Wireless Mouse", 5, "S1")

    def test_01_stock_availability(self):
        self.system.add_stock("Warehouse A", "P100", 10)
        ok, msg = self.system.fulfill_order("P100", 4)
        self.assertTrue(ok)
        self.assertIn("Fulfilled by Warehouse A", msg)

    def test_02_insufficient_inventory(self):
        self.system.add_stock("Warehouse A", "P100", 3)
        ok, msg = self.system.fulfill_order("P100", 5)
        self.assertFalse(ok)
        self.assertEqual(msg, "Insufficient inventory")

    def test_03_warehouse_transfer(self):
        self.system.add_stock("Warehouse A", "P100", 10)
        self.system.transfer_stock("Warehouse A", "Warehouse B", "P100", 4)
        self.assertEqual(
            self.system.warehouses["Warehouse A"].inventory["P100"], 6)
        self.assertEqual(
            self.system.warehouses["Warehouse B"].inventory["P100"], 4)

    def test_04_concurrent_orders(self):
        self.system.add_stock("Warehouse A", "P100", 10)

        def order():
            self.system.fulfill_order("P100", 1)

        threads = [threading.Thread(target=order) for _ in range(12)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        total = sum(w.inventory.get("P100", 0)
                    for w in self.system.warehouses.values())
        self.assertEqual(total, 0)

    def test_05_reorder_threshold(self):
        self.system.add_stock("Warehouse A", "P100", 6)
        ok, msg = self.system.fulfill_order("P100", 3)
        self.assertTrue(ok)
        self.assertIn("Low stock alert", msg)

    def test_06_invalid_product(self):
        ok, msg = self.system.fulfill_order("INVALID_ID", 1)
        self.assertFalse(ok)
        self.assertEqual(msg, "Invalid product")

    def test_07_negative_inventory(self):
        self.system.add_stock("Warehouse A", "P100", 5)
        with self.assertRaises(ValueError):
            self.system.warehouses["Warehouse A"].remove_stock("P100", 10)

    def test_08_multiple_warehouses(self):
        self.system.add_stock("Warehouse A", "P100", 2)
        self.system.add_stock("Warehouse B", "P100", 10)
        ok, msg = self.system.fulfill_order("P100", 5)
        self.assertTrue(ok)
        self.assertIn("Fulfilled by Warehouse B", msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)