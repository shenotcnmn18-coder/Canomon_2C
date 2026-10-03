class Payment:
    """Base class for all payment methods."""

    method = "Unknown"

    def __init__(self):
        self.amount_paid = 0.0
        self.change = 0.0

    def process(self, total):
        raise NotImplementedError("Subclasses must implement process().")


class CashPayment(Payment):
    method = "Cash"

    def __init__(self, amount_tendered):
        super().__init__()
        self.amount_tendered = amount_tendered

    def process(self, total):
        if self.amount_tendered < total:
            raise ValueError(f"Insufficient cash. Short by ₱{total - self.amount_tendered:.2f}.")
        self.amount_paid = self.amount_tendered
        self.change = self.amount_tendered - total
        return self.change


class CardPayment(Payment):
    method = "Card"

    def process(self, total):
        # Simulated card approval: always exact amount, no change.
        self.amount_paid = total
        self.change = 0.0
        return self.change