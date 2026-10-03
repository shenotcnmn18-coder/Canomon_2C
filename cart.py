class CartItem:
    """A product and the quantity being bought."""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Cart:
    """Holds the items a customer wants to buy."""

    def __init__(self):
        self.items = {}  # product_id -> CartItem

    def add_item(self, product, quantity):
        current_qty = self.items[product.product_id].quantity if product.product_id in self.items else 0
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        if current_qty + quantity > product.stock:
            raise ValueError(f"Not enough stock. Only {product.stock} available.")

        if product.product_id in self.items:
            self.items[product.product_id].quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product, quantity)

    def remove_item(self, product_id):
        if product_id not in self.items:
            raise ValueError("That product is not in the cart.")
        del self.items[product_id]

    def get_total(self):
        return sum(item.subtotal for item in self.items.values())

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items.clear()

    def show(self):
        if self.is_empty():
            print("Cart is empty.")
            return
        print(f"\n{'ID':<4}{'Item':<20}{'Qty':>4}{'Price':>10}{'Subtotal':>12}")
        print("-" * 50)
        for pid, item in self.items.items():
            print(f"{pid:<4}{item.product.name:<20}{item.quantity:>4}"
                  f"{item.product.price:>10.2f}{item.subtotal:>12.2f}")
        print("-" * 50)
        print(f"{'TOTAL':<38}{self.get_total():>12.2f}")