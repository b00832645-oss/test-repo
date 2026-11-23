import pytest
from inheritance import Vehicle, Car, Bicycle, Person, Student, Employee, BankAccount, SavingsAccount


def test_vehicle_polymorphism():
    assert [v.drive() for v in (Vehicle(), Car(), Bicycle())] == [
        "Driving a vehicle", "Driving a car", "Riding a bicycle"]


def test_student_and_employee_keep_parent_attributes():
    s = Student("Ann", 20, "Paris", "AI")
    e = Employee("Bob", 35, "Lyon", "EDF")
    assert (s.name, s.age, s.address) == ("Ann", 20, "Paris")
    assert isinstance(s, Person) and isinstance(e, Person)
    assert "study AI" in s.introduce()
    assert "work at EDF" in e.introduce()


def test_transfer_success():
    a, b = SavingsAccount("A", 1000), SavingsAccount("B", 200)
    assert a.transfer(b, 300) is True
    assert (a.check_balance(), b.check_balance()) == (700, 500)


def test_transfer_insufficient_balance_changes_nothing():
    a, b = SavingsAccount("A", 100), SavingsAccount("B", 0)
    assert a.transfer(b, 500) is False
    assert (a.check_balance(), b.check_balance()) == (100, 0)


def test_add_interest_uses_deposit():
    acc = SavingsAccount("A", 1000, interest_rate=0.05)
    assert acc.add_interest() == 50
    assert acc.check_balance() == 1050


def test_savings_is_a_bank_account():
    assert issubclass(SavingsAccount, BankAccount)


def test_withdraw_returns_false_when_insufficient():
    assert BankAccount("X", 10).withdraw(50) is False
