"""Unit tests: one function in isolation, fast, no external dependency."""
import pytest
from shop import calculate_discount, calculate_tax, calculate_total


class TestUnitDiscount:
    @pytest.mark.parametrize("price, pct, expected", [
        (100, 10, 90.0),        # standard case
        (50, 0, 50.0),          # no discount
        (75, 100, 0.0),         # free
        (19.99, 15, 16.99),     # decimals
    ])
    def test_discount_values(self, price, pct, expected):
        # Arrange (parameters) / Act / Assert
        assert calculate_discount(price, pct) == expected

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10, 20)

    @pytest.mark.parametrize("pct", [-1, 150])
    def test_invalid_discount_raises(self, pct):
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100, pct)


class TestUnitTax:
    def test_default_20_percent(self):
        assert calculate_tax(100) == 20.0

    def test_custom_rate(self):
        assert calculate_tax(100, 0.10) == 10.0

    def test_zero_price(self):
        assert calculate_tax(0) == 0.0


class TestUnitTotal:
    def test_single_item(self):
        assert calculate_total([50.0]) == 60.0                 # 50 + 20 % tax

    def test_multiple_items(self):
        assert calculate_total([10.0, 20.0, 30.0]) == 72.0     # 60 + 12

    def test_empty_cart(self):
        assert calculate_total([]) == 0.0

    def test_float_precision(self):
        assert calculate_total([0.1, 0.2]) == pytest.approx(0.36)
