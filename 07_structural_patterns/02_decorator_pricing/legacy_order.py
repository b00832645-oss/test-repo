"""Starting code from the course exercise (kept for comparison; do not use)."""


class Order:
    def __init__(self, base_price: float):
        self.base_price = base_price

    def calculate_total(self, has_express_shipping=False, has_insurance=False, has_gift_wrap=False,
                        discount_percent=0, is_premium_member=False) -> float:
        total = self.base_price
        if has_express_shipping:
            total += 15.00
        if has_insurance:
            total += self.base_price * 0.05
        if has_gift_wrap:
            total += 5.00
        if discount_percent > 0:
            total -= total * (discount_percent / 100)
        if is_premium_member:
            total -= total * 0.10
        return total
