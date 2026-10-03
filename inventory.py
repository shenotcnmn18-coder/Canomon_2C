from product import Product


class Inventory:
    """Manages products and stock levels in the database."""

    def __init__(self, database):
        self.db = database
        self.add_sample_products()

    def add_sample_products(self):
        """Adds starter products only if the table is empty."""
        if self.db.fetch_one("SELECT id FROM products"):
            return
        samples = [
            ("Bottled Water", 15.00, 50),
            ("Instant Noodles", 12.50, 40),
            ("Coffee Sachet", 8.00, 100),
            ("Bread Loaf", 55.00, 20),
            ("Canned Sardines", 28.00, 30),
        ]
        for name, price, stock in samples:
            self.add_product(name, price, stock)

    def add_product(self, name, price, stock):
        self.db.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock),
        )

    def get_product(self, product_id):
        row = self.db.fetch_one("SELECT * FROM products WHERE id = ?", (product_id,))
        if row is None:
            return None
        return Product(row["id"], row["name"], row["price"], row["stock"])

    def get_all_products(self):
        rows = self.db.fetch_all("SELECT * FROM products ORDER BY id")
        return [Product(r["id"], r["name"], r["price"], r["stock"]) for r in rows]

    def restock(self, product_id, quantity):
        self.db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (quantity, product_id),
        )

    def reduce_stock(self, product_id, quantity):
        self.db.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (quantity, product_id),
        )