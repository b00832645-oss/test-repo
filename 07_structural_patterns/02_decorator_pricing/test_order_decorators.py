import pytest
from legacy_order import Order
from order_decorators import (BaseOrder, OrderComponent, ExpressShippingDecorator, InsuranceDecorator,
                              GiftWrapDecorator, DiscountDecorator, PremiumMemberDecorator)


def test_base_order():
    assert BaseOrder(100).get_cost() == 100


def test_full_stack_matches_legacy_total():
    order = PremiumMemberDecorator(DiscountDecorator(GiftWrapDecorator(InsuranceDecorator(
        ExpressShippingDecorator(BaseOrder(100.0)))), percent=15))
    legacy = Order(100.0).calculate_total(True, True, True, 15, True)
    assert order.get_cost() == pytest.approx(legacy) == pytest.approx(95.625)


@pytest.mark.parametrize("deco, expected", [
    (ExpressShippingDecorator, 115), (InsuranceDecorator, 105), (GiftWrapDecorator, 105),
    (PremiumMemberDecorator, 90)])
def test_each_decorator_alone(deco, expected):
    assert deco(BaseOrder(100)).get_cost() == pytest.approx(expected)


def test_order_of_wrapping_matters():
    a = DiscountDecorator(ExpressShippingDecorator(BaseOrder(100)), percent=10)   # (100+15)*0.9
    b = ExpressShippingDecorator(DiscountDecorator(BaseOrder(100), percent=10))   # 100*0.9+15
    assert a.get_cost() == pytest.approx(103.5)
    assert b.get_cost() == pytest.approx(105.0)


def test_decorators_are_order_components():
    assert isinstance(GiftWrapDecorator(BaseOrder(1)), OrderComponent)


def test_description_lists_every_layer():
    desc = GiftWrapDecorator(ExpressShippingDecorator(BaseOrder(100))).get_description()
    assert desc.splitlines() == ["Base price: 100.00€", "Express shipping: +15.00€", "Gift wrap: +5.00€"]


def test_invalid_discount():
    with pytest.raises(ValueError):
        DiscountDecorator(BaseOrder(100), percent=150)
