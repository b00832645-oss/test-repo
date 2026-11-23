"""Starting code from the course exercise (kept for comparison; do not use)."""


def process_payment(payment_type: str, amount: float, details: dict):
    if payment_type == "credit_card":
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        if not card_number or len(card_number) != 16:
            return {"success": False, "error": "Invalid card number"}
        if not cvv or len(cvv) != 3:
            return {"success": False, "error": "Invalid CVV"}
        fee = amount * 0.029
        return {"success": True, "method": "credit_card", "amount": amount + fee, "fee": fee}
    elif payment_type == "bank_transfer":
        iban = details.get("iban")
        if not iban or len(iban) < 15:
            return {"success": False, "error": "Invalid IBAN"}
        fee = 1.50
        return {"success": True, "method": "bank_transfer", "amount": amount + fee, "fee": fee}
    elif payment_type == "paypal":
        email = details.get("email")
        if not email or "@" not in email:
            return {"success": False, "error": "Invalid PayPal email"}
        fee = amount * 0.034 + 0.30
        return {"success": True, "method": "paypal", "amount": amount + fee, "fee": fee}
    else:
        return {"success": False, "error": f"Unknown payment type: {payment_type}"}
