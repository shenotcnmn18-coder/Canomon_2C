from datetime import datetime


class Transaction:
    """Completes a sale: processes payment, saves records, updates stock."""

    def __init__(self, database, inventory, cart, payment):
        self.db = database
        self.inventory = inventory
        self.cart = cart
        self.payment = payment
        self.transaction_id = None
        self.date = None
        self.total = 0.0

    def complete(self):
        if self.cart.is_empty():
            raise ValueError("Cannot checkout an empty cart.")

        self.total = self.cart.get_total()
        self.payment.process(self.total)  # raises ValueError if payment fails
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.db.execute(
            """INSERT INTO transactions
               (date, total, payment_method, amount_paid, change_due)
               VALUES (?, ?, ?, ?, ?)""",
            (self.date, self.total, self.payment.method,
             self.payment.amount_paid, self.payment.change),
        )
        self.transaction_id = cursor.lastrowid

        for item in self.cart.items.values():
            self.db.execute(
                """INSERT INTO transaction_items
                   (transaction_id, product_name, price, quantity)
                   VALUES (?, ?, ?, ?)""",
                (self.transaction_id, item.product.name, item.product.price, item.quantity),
            )
            self.inventory.reduce_stock(item.product.product_id, item.quantity)