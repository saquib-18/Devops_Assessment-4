import threading
from typing import Dict, List, Optional, Tuple

class Product:
    def __init__(self, product_id: str, name: str, reorder_threshold: int, supplier_name: str):
        self.product_id = product_id
        self.name = name
        self.reorder_threshold = reorder_threshold
        self.supplier_name = supplier_name

class Warehouse:
    def __init__(self, name: str):
        self.name = name
        self.stock: Dict[str, int] = {}  # product_id -> quantity

    def add_stock(self, product_id: str, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity to add cannot be negative.")
        self.stock[product_id] = self.stock.get(product_id, 0) + quantity

    def remove_stock(self, product_id: str, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity to remove cannot be negative.")
        current_stock = self.stock.get(product_id, 0)
        if current_stock < quantity:
            raise ValueError(f"Insufficient inventory in {self.name}.")
        self.stock[product_id] = current_stock - quantity

class InventorySystem:
    def __init__(self):
        self.lock = threading.Lock()
        self.products: Dict[str, Product] = {}
        self.warehouses: Dict[str, Warehouse] = {
            "Warehouse A": Warehouse("Warehouse A"),
            "Warehouse B": Warehouse("Warehouse B"),
            "Warehouse C": Warehouse("Warehouse C")
        }
        self.suppliers: Dict[str, List[str]] = {}  # supplier_name -> list of product_ids

    # 1. Supplier Management & Register Product
    def register_product(self, product_id: str, name: str, reorder_threshold: int, supplier_name: str):
        with self.lock:
            product = Product(product_id, name, reorder_threshold, supplier_name)
            self.products[product_id] = product
            if supplier_name not in self.suppliers:
                self.suppliers[supplier_name] = []
            if product_id not in self.suppliers[supplier_name]:
                self.suppliers[supplier_name].append(product_id)

    # 2. Add Product Stock
    def add_product_stock(self, warehouse_name: str, product_id: str, quantity: int):
        with self.lock:
            if product_id not in self.products:
                raise ValueError("Invalid product: Product not registered.")
            if warehouse_name not in self.warehouses:
                raise ValueError("Invalid warehouse name.")
            self.warehouses[warehouse_name].add_stock(product_id, quantity)

    # 3. Warehouse Selection & Remove Product (Order Fulfillment)
    def fulfill_order(self, product_id: str, quantity: int) -> str:
        with self.lock:
            if product_id not in self.products:
                raise ValueError("Invalid product: Product not registered.")
            if quantity < 0:
                raise ValueError("Negative inventory requested.")

            # Automatic Warehouse Selection (finds the first warehouse with enough stock)
            selected_warehouse: Optional[str] = None
            for wh_name, wh in self.warehouses.items():
                if wh.stock.get(product_id, 0) >= quantity:
                    selected_warehouse = wh_name
                    break
            
            if not selected_warehouse:
                raise ValueError("Insufficient inventory across all individual warehouses.")
            
            self.warehouses[selected_warehouse].remove_stock(product_id, quantity)
            return selected_warehouse

    # 4. Transfer Stock
    def transfer_stock(self, from_warehouse: str, to_warehouse: str, product_id: str, quantity: int):
        with self.lock:
            if from_warehouse not in self.warehouses or to_warehouse not in self.warehouses:
                raise ValueError("Invalid warehouse selection.")
            if product_id not in self.products:
                raise ValueError("Invalid product: Product not registered.")
            
            self.warehouses[from_warehouse].remove_stock(product_id, quantity)
            self.warehouses[to_warehouse].add_stock(product_id, quantity)

    # 5. Low-Stock Detection & Reorder System
    def check_and_reorder(self) -> List[Tuple[str, str, int]]:
        with self.lock:
            reordered_items = []
            for product_id, product in self.products.items():
                # Calculate total stock across all warehouses
                total_stock = sum(wh.stock.get(product_id, 0) for wh in self.warehouses.values())
                
                if total_stock <= product.reorder_threshold:
                    # Simulate reorder process: top-up by a fixed amount (e.g., 50 units) to Warehouse A
                    reorder_amount = 50
                    self.warehouses["Warehouse A"].add_stock(product_id, reorder_amount)
                    reordered_items.append((product_id, product.supplier_name, reorder_amount))
            return reordered_items
