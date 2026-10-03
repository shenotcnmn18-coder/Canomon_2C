from database import Database
from inventory import Inventory
from cart import Cart
from payment import CashPayment, CardPayment
from transaction import Transaction
from receipt import Receipt


class POSApp:
    """Console menu that ties all the modules together."""

    def __init__(self):
        self.db = Database()
        self.inventory = Inventory(self.db)
        self.cart = Cart()

    # ---------- input helpers ----------
    @staticmethod
    def ask_int(message):
        try:
            return int(input(message))
        except ValueError:
            raise ValueError("Please enter a whole number.")

    @staticmethod
    def ask_float(message):
        try:
            return float(input(message))
        except ValueError:
            raise ValueError("Please enter a valid number.")

    # ---------- menu actions ----------
    def view_products(self):
        print("\n--- PRODUCTS ---")
        for product in self.inventory.get_all_products():
            print(product)

    def add_to_cart(self):
        self.view_products()
        product_id = self.ask_int("\nProduct ID: ")
        product = self.inventory.get_product(product_id)
        if product is None:
            raise ValueError("Product not found.")
        quantity = self.ask_int("Quantity: ")
        self.cart.add_item(product, quantity)
        print(f"Added {quantity} x {product.name} to cart.")

    def remove_from_cart(self):
        self.cart.show()
        if not self.cart.is_empty():
            self.cart.remove_item(self.ask_int("\nProduct ID to remove: "))
            print("Item removed.")

    def checkout(self):
        if self.cart.is_empty():
            raise ValueError("Cart is empty.")
        self.cart.show()

        method = input("\nPayment method (1 = Cash, 2 = Card): ").strip()
        if method == "1":
            payment = CashPayment(self.ask_float("Cash received: ₱"))
        elif method == "2":
            payment = CardPayment()
        else:
            raise ValueError("Invalid payment method.")

        transaction = Transaction(self.db, self.inventory, self.cart, payment)
        transaction.complete()
        Receipt(transaction).print_receipt()
        self.cart = Cart()  # fresh cart for the next customer

    def add_new_product(self):
        name = input("Product name: ").strip()
        price = self.ask_float("Price: ₱")
        stock = self.ask_int("Starting stock: ")
        if not name or price <= 0 or stock < 0:
            raise ValueError("Invalid product details.")
        self.inventory.add_product(name, price, stock)
        print("Product added.")

    def restock_product(self):
        self.view_products()
        product_id = self.ask_int("\nProduct ID: ")
        if self.inventory.get_product(product_id) is None:
            raise ValueError("Product not found.")
        quantity = self.ask_int("Quantity to add: ")
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.inventory.restock(product_id, quantity)
        print("Stock updated.")

    # ---------- main loop ----------
    def run(self):
        actions = {
            "1": self.view_products,
            "2": self.add_to_cart,
            "3": self.cart_show,
            "4": self.remove_from_cart,
            "5": self.checkout,
            "6": self.add_new_product,
            "7": self.restock_product,
        }

        while True:
            print("""
===== POINT OF SALE =====
1. View Products
2. Add to Cart
3. View Cart
4. Remove from Cart
5. Checkout
6. Add New Product
7. Restock Product
0. Exit""")
            choice = input("Choose: ").strip()

            if choice == "0":
                self.db.close()
                print("Goodbye!")
                break
            if choice not in actions:
                print("Invalid choice.")
                continue

            try:
                actions[choice]()
            except ValueError as error:
                print(f"Error: {error}")

    def cart_show(self):
        self.cart.show()


if __name__ == "__main__":
    POSApp().run()