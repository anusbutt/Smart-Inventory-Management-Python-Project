import json
from datetime import datetime

class Product:
    def __init__(self, sku, name, category, price, stock, created_at=None):
        self.sku = sku
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at
        }
class Inventory:
    def __init__(self, db_path="database.json"):
        self.db_path = db_path
        self.products = self.load_data()

    def load_data(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return {k: Product(**v) for k, v in data.items()}
        except FileNotFoundError:
            return {}

    def save_data(self):
        data = {k: v.to_dict() for k, v in self.products.items()}
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)

    def add_product(self, product):
        if product.sku in self.products:
            raise ValueError("SKU already exists.")
        self.products[product.sku] = product
        self.save_data()

    def update_stock(self, sku, amount):
        if sku in self.products:
            self.products[sku].stock += amount
            self.save_data()
        else:
            raise ValueError("Product not found.")

    def get_product(self, sku):
        return self.products.get(sku)

    def get_all(self):
        return self.products.values()

    def get_low_stock(self, threshold=5):
        return [p for p in self.products.values() if p.stock <= threshold]
