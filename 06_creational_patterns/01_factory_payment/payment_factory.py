"""Factory Method refactoring of the payment system."""
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Interface every payment processor promises to follow."""

    name: str = "abstract"
    error_message: str = "Invalid payment details"

    @abstractmethod
    def validate(self, details: dict) -> bool: ...

    @abstractmethod
    def fee(self, amount: float) -> float: ...

    def process(self, amount: float, details: dict) -> dict:
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        if not self.validate(details):
            return {"success": False, "error": self.error_message}
        fee = round(self.fee(amount), 2)
        return {"success": True, "method": self.name, "amount": round(amount + fee, 2), "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    name = "credit_card"
    error_message = "Invalid card number or CVV"

    def validate(self, details: dict) -> bool:
        card, cvv = details.get("card_number", ""), details.get("cvv", "")
        return len(card) == 16 and card.isdigit() and len(cvv) == 3 and cvv.isdigit()

    def fee(self, amount: float) -> float:
        return amount * 0.029                      # 2.9 %


class BankTransferProcessor(PaymentProcessor):
    name = "bank_transfer"
    error_message = "Invalid IBAN"

    def validate(self, details: dict) -> bool:
        return len(details.get("iban", "")) >= 15

    def fee(self, amount: float) -> float:
        return 1.50                                # flat fee


class PayPalProcessor(PaymentProcessor):
    name = "paypal"
    error_message = "Invalid PayPal email"

    def validate(self, details: dict) -> bool:
        return "@" in details.get("email", "")

    def fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30               # 3.4 % + 0.30 €


class PaymentFactory:
    """Maps a payment type string to the right processor class."""

    _processors: dict[str, type[PaymentProcessor]] = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def register(cls, payment_type: str, processor_cls: type[PaymentProcessor]) -> None:
        """Add a new payment method without modifying existing code (Open/Closed)."""
        cls._processors[payment_type] = processor_cls

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            return self._processors[payment_type]()
        except KeyError:
            raise ValueError(f"Unknown payment type: {payment_type}") from None


if __name__ == "__main__":
    factory = PaymentFactory()
    print(factory.get_processor("credit_card").process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))
    print(factory.get_processor("bank_transfer").process(100.0, {"iban": "FR7630006000011234567890189"}))
    print(factory.get_processor("paypal").process(100.0, {"email": "louis@example.com"}))
