class Receipt:
    """Builds a printable receipt from a completed transaction."""

    WIDTH = 42

    def __init__(self, transaction, store_name="PYTHON MINI MART"):
        self.transaction = transaction
        self.store_name = store_name

    def generate(self):
        t = self.transaction
        line = "=" * self.WIDTH
        dash = "-" * self.WIDTH

        lines = [
            line,
            self.store_name.center(self.WIDTH),
            "OFFICIAL RECEIPT".center(self.WIDTH),
            line,
            f"Receipt #: {t.transaction_id:05d}",
            f"Date     : {t.date}",
            dash,
        ]
        for item in t.cart.items.values():
            lines.append(f"{item.product.name} x{item.quantity}")
            lines.append(f"{'@ ' + format(item.product.price, '.2f'):>20}{item.subtotal:>22.2f}")
        lines += [
            dash,
            f"{'TOTAL':<20}{t.total:>22.2f}",
            f"{t.payment.method + ' Paid':<20}{t.payment.amount_paid:>22.2f}",
            f"{'Change':<20}{t.payment.change:>22.2f}",
            line,
            "Thank you for shopping!".center(self.WIDTH),
            line,
        ]
        return "\n".join(lines)

    def print_receipt(self):
        print("\n" + self.generate() + "\n")