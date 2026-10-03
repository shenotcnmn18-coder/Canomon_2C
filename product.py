class Product:
    """Represents a single product for sale."""

    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"[{self.product_id}] {self.name:<20} ₱{self.price:>8.2f}   Stock: {self.stock}"