"""Property-based tests: Hypothesis generates many inputs to try to break each rule."""
import pytest

hypothesis = pytest.importorskip("hypothesis")
from hypothesis import given, strategies as st

from shop import calculate_discount, calculate_total

prices = st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False)
percents = st.floats(min_value=0, max_value=100, allow_nan=False)


@given(prices, percents)
def test_discount_never_increases_price(price, pct):
    assert calculate_discount(price, pct) <= round(price, 2) + 0.01


@given(prices)
def test_zero_discount_keeps_price(price):
    assert calculate_discount(price, 0) == round(price, 2)


@given(st.lists(prices, max_size=20))
def test_total_is_at_least_the_subtotal(items):
    assert calculate_total(items) >= round(sum(items), 2) - 0.01
