import pytest
from payment_factory import (PaymentFactory, PaymentProcessor, CreditCardProcessor,
                             BankTransferProcessor, PayPalProcessor)


@pytest.fixture
def factory():
    return PaymentFactory()


@pytest.mark.parametrize("ptype, cls", [("credit_card", CreditCardProcessor),
                                        ("bank_transfer", BankTransferProcessor),
                                        ("paypal", PayPalProcessor)])
def test_factory_returns_right_class(factory, ptype, cls):
    assert isinstance(factory.get_processor(ptype), cls)


def test_unknown_type_raises(factory):
    with pytest.raises(ValueError, match="Unknown payment type"):
        factory.get_processor("crypto")


@pytest.mark.parametrize("ptype, details, total, fee", [
    ("credit_card", {"card_number": "1234567890123456", "cvv": "123"}, 102.9, 2.9),
    ("bank_transfer", {"iban": "FR7630006000011234567890189"}, 101.5, 1.5),
    ("paypal", {"email": "a@b.com"}, 103.7, 3.7),
])
def test_fees_match_legacy_rules(factory, ptype, details, total, fee):
    result = factory.get_processor(ptype).process(100.0, details)
    assert result == {"success": True, "method": ptype, "amount": total, "fee": fee}


@pytest.mark.parametrize("ptype, details", [("credit_card", {"card_number": "123", "cvv": "123"}),
                                            ("bank_transfer", {"iban": "FR76"}),
                                            ("paypal", {"email": "nope"})])
def test_invalid_details(factory, ptype, details):
    assert factory.get_processor(ptype).process(100.0, details)["success"] is False


def test_register_new_method_without_editing_factory(factory):
    class ApplePayProcessor(PaymentProcessor):
        name = "apple_pay"
        def validate(self, details): return details.get("token") is not None
        def fee(self, amount): return 0.0

    PaymentFactory.register("apple_pay", ApplePayProcessor)
    assert factory.get_processor("apple_pay").process(50, {"token": "x"})["amount"] == 50
