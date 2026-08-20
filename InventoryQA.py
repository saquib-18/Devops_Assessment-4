import unittest
import threading
from InventoryManagement import InventorySystem

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.system = InventorySystem()
        # Register a base product for testing
        self.system.register_product("P101", "Widget A", reorder_threshold=10, supplier_name="Global Supplier Co")

    # 1. Test Stock Availability
    def test_stock_availability(self):
        self.system.add_product_stock("Warehouse A", "P101", 20)
        wh = self.system.fulfill_order("P101", 5)
        self.assertEqual(wh, "Warehouse A")
        self.assertEqual(self.system.warehouses["Warehouse A"].stock["P101"], 15)

    # 2. Test Insufficient Inventory
    def test_insufficient_inventory(self):
        self.system.add_product_stock("Warehouse A", "P101", 5)
        with self.assertRaises(ValueError):
            self.system.fulfill_order("P101", 10)

    # 3. Test Warehouse Transfer
    def test_warehouse_transfer(self):
        self.system.add_product_stock("Warehouse A", "P101", 30)
        self.system.transfer_stock("Warehouse A", "Warehouse B", "P101", 10)
        self.assertEqual(self.system.warehouses["Warehouse A"].stock["P101"], 20)
        self.assertEqual(self.system.warehouses["Warehouse B"].stock["P101"], 10)

    # 4. Test Concurrent Orders (Thread Safety)
    def test_concurrent_orders(self):
        self.system.add_product_stock("Warehouse A", "P101", 100)
        
        def place_order():
            try:
                self.system.fulfill_order("P101", 10)
            except ValueError:
                pass

        threads = [threading.Thread(target=place_order) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 10 orders of 10 should deplete exactly 100 units
        self.assertEqual(self.system.warehouses["Warehouse A"].stock["P101"], 0)

    # 5. Test Reorder Threshold & Low-Stock Detection
    def test_reorder_threshold(self):
        self.system.add_product_stock("Warehouse A", "P101", 8)  # Below threshold of 10
        reorders = self.system.check_and_reorder()
        self.assertEqual(len(reorders), 1)
        self.assertEqual(reorders[0][0], "P101")
        # Warehouse A stock should now be original 8 + 50 reordered units
        self.assertEqual(self.system.warehouses["Warehouse A"].stock["P101"], 58)

    # 6. Test Invalid Product
    def test_invalid_product(self):
        with self.assertRaises(ValueError):
            self.system.add_product_stock("Warehouse A", "INVALID_ID", 10)
        with self.assertRaises(ValueError):
            self.system.fulfill_order("INVALID_ID", 5)

    # 7. Test Negative Inventory
    def test_negative_inventory(self):
        with self.assertRaises(ValueError):
            self.system.fulfill_order("P101", -5)
        with self.assertRaises(ValueError):
            self.system.add_product_stock("Warehouse A", "P101", -10)

    # 8. Test Multiple Warehouses Selection
    def test_multiple_warehouses_selection(self):
        # Warehouse A has 5 units, Warehouse B has 20 units
        self.system.add_product_stock("Warehouse A", "P101", 5)
        self.system.add_product_stock("Warehouse B", "P101", 20)
        
        # Order of 15 cannot be fulfilled by A, should automatically target B
        selected_wh = self.system.fulfill_order("P101", 15)
        self.assertEqual(selected_wh, "Warehouse B")
        self.assertEqual(self.system.warehouses["Warehouse B"].stock["P101"], 5)

if __name__ == "__main__":
    unittest.main()
