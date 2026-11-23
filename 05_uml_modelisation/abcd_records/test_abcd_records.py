import pytest
from abcd_records import (RoyalMember, RegularMember, CD, Tape, OrderProcessingClerk, CollectionClerk,
                          DailyRecords, MembershipApplication, CashPayment, CheckPayment, BankDraftPayment)


@pytest.fixture
def clerk():
    return OrderProcessingClerk({"R1": RoyalMember("R1", "Rita", "Paris"),
                                 "G1": RegularMember("G1", "Greg", "Lyon")})


def test_non_member_gets_application(clerk):
    assert isinstance(clerk.process("X9", []), MembershipApplication)


def test_royal_scenario_two_cds_one_unavailable_paid_by_check(clerk):
    a, b = CD("C1", "Kind of Blue", 15, 3), CD("C2", "Blue Train", 12, 0)
    order = clerk.process("R1", [(a, 1), (b, 1)])
    assert [l.back_ordered for l in order.lines] == [False, True]
    assert order.total() == pytest.approx((15 + 12) * 0.9)
    assert order.shipping_list() == ["1 x Kind of Blue"]
    records = DailyRecords()
    assert CollectionClerk(records).collect(order, CheckPayment("004512")) is True
    assert order.status == "paid" and records.orders == [order]


def test_regular_member_cannot_order_unavailable(clerk):
    with pytest.raises(ValueError, match="unavailable"):
        clerk.process("G1", [(Tape("T1", "Mixtape", 5, 0), 1)])


def test_regular_member_pays_full_price(clerk):
    order = clerk.process("G1", [(CD("C1", "X", 10, 5), 2)])
    assert order.total() == 20


def test_stock_decreases(clerk):
    cd = CD("C1", "X", 10, 5)
    clerk.process("G1", [(cd, 2)])
    assert cd.stock == 3


@pytest.mark.parametrize("payment, ok", [(CashPayment(), True), (CheckPayment("12"), True),
                                         (CheckPayment("??"), False), (BankDraftPayment("BD-1"), True),
                                         (BankDraftPayment("X"), False)])
def test_refused_payment_puts_order_on_hold(clerk, payment, ok):
    order = clerk.process("G1", [(CD("C1", "X", 10, 5), 1)])
    records = DailyRecords()
    assert CollectionClerk(records).collect(order, payment) is ok
    assert order.status == ("paid" if ok else "on hold")
