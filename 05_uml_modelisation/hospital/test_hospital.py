import pytest
from hospital import (Organizer, Patient, Doctor, ProblemStatus,
                      CashPayment, CheckPayment, CreditCardPayment)


@pytest.fixture
def world():
    org = Organizer("Olivia", "admin")
    pat = Patient("Paul", "pw")
    doc = Doctor("Dr Diane", "pw", "GP")
    org.register_member(pat)
    org.register_member(doc)
    return org, pat, doc


def test_full_consultation_flow(world):
    org, pat, doc = world
    problem = pat.submit_problem("cough")
    assert problem.status is ProblemStatus.PENDING
    org.assign(problem, doc)
    assert problem.status is ProblemStatus.IN_REVIEW
    rx = doc.write_prescription(problem, "syrup", 40)
    org.send_prescription(rx)
    assert pat.inbox == [rx]
    payment = pat.pay(rx, CashPayment())
    org.forward_payment(payment)
    assert doc.balance == 40
    assert problem.status is ProblemStatus.RESOLVED


@pytest.mark.parametrize("method, ok", [
    (CashPayment(), True),
    (CheckPayment("123456"), True),
    (CheckPayment("abc"), False),
    (CreditCardPayment("4242424242424242"), True),
    (CreditCardPayment("42"), False),
])
def test_payment_strategies(method, ok):
    assert method.process(40) is ok


def test_refused_payment_raises(world):
    org, pat, doc = world
    problem = pat.submit_problem("cough")
    org.assign(problem, doc)
    rx = doc.write_prescription(problem, "syrup", 40)
    with pytest.raises(ValueError, match="refused"):
        pat.pay(rx, CreditCardPayment("1"))


def test_payment_forwarded_only_once(world):
    org, pat, doc = world
    problem = pat.submit_problem("cough")
    org.assign(problem, doc)
    payment = pat.pay(doc.write_prescription(problem, "x", 40), CashPayment())
    org.forward_payment(payment)
    with pytest.raises(ValueError):
        org.forward_payment(payment)
    assert doc.balance == 40


def test_doctor_cannot_prescribe_unassigned_problem(world):
    org, pat, doc = world
    problem = pat.submit_problem("cough")
    with pytest.raises(PermissionError):
        doc.write_prescription(problem, "x", 10)


def test_login(world):
    _, pat, _ = world
    assert pat.login("pw") is True
    assert pat.login("wrong") is False
