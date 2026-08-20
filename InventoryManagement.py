import threading

class Product:
    def __init__(self, product_id, name, reorder_threshold):
        self.product_id = product_id
        self.name = name
        self.reorder_threshold = reorder_threshold

class Supplier:
    def __init__(self, supplier_id, name):
        self.supplier_id = supplier_id
        self.name = name
        self.managed_products = []

class Warehouse:
    def __init__(self, name):
        self.name = name
        self.inventory = {}

    def add_stock(self, product_id, qty):
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        self.inventory[product_id] = self.inventory.get(product_id, 0) + qty

    def remove_stock(self, product_id, qty):
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        if self.inventory.get(product_id, 0) < qty:
            raise ValueError("Insufficient inventory: stock cannot be negative")
        self.inventory[product_id] -= qty


class InventorySystem:
    def __init__(self):
        self.products = {}
        self.suppliers = {}
        self.warehouses = {
            "Warehouse A": Warehouse("Warehouse A"),
            "Warehouse B": Warehouse("Warehouse B"),
            "Warehouse C": Warehouse("Warehouse C")
        }
        self.product_supplier_map = {}
        self.lock = threading.Lock()

    def add_supplier(self, supplier_id, name):
        self.suppliers[supplier_id] = Supplier(supplier_id, name)

    def add_product(self, product_id, name, threshold, supplier_id=None):
        self.products[product_id] = Product(product_id, name, threshold)
        if supplier_id in self.suppliers:
            self.product_supplier_map[product_id] = supplier_id
            self.suppliers[supplier_id].managed_products.append(product_id)

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
        for wh in self.warehouses.values():
            wh.inventory.pop(product_id, None)

    def add_stock(self, warehouse, product_id, qty):
        if product_id not in self.products:
            raise ValueError("Invalid product")
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")
        self.warehouses[warehouse].add_stock(product_id, qty)

    def transfer_stock(self, source, target, product_id, qty):
        if source not in self.warehouses or target not in self.warehouses:
            raise ValueError("Invalid warehouse choice")
        self.warehouses[source].remove_stock(product_id, qty)
        self.warehouses[target].add_stock(product_id, qty)

    def detect_low_stock(self, product_id):
        if product_id not in self.products:
            raise ValueError("Invalid product")
        total = sum(w.inventory.get(product_id, 0)
                    for w in self.warehouses.values())
        return total < self.products[product_id].reorder_threshold

    def trigger_reorder(self, product_id):
        sid = self.product_supplier_map.get(product_id)
        if sid:
            return f"Reorder triggered with Supplier {self.suppliers[sid].name}"
        return "Reorder triggered (No supplier assigned)"

    def select_warehouse(self, product_id, qty):
        for name in ["Warehouse A", "Warehouse B", "Warehouse C"]:
            if self.warehouses[name].inventory.get(product_id, 0) >= qty:
                return name
        return None

    def fulfill_order(self, product_id, qty):
        if product_id not in self.products:
            return False, "Invalid product"

        warehouse = self.select_warehouse(product_id, qty)

        if not warehouse:
            return False, "Insufficient inventory"

        self.warehouses[warehouse].remove_stock(product_id, qty)
        msg = f"Fulfilled by {warehouse}"

        if self.detect_low_stock(product_id):
            msg += " | Low stock alert: " + self.trigger_reorder(product_id)

        return True, msg