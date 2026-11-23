import math
import pytest
from basics import Rectangle, Circle, Account, Book, Movie


def test_rectangle_area():
    assert Rectangle(3, 4).area() == 12


def test_rectangle_rejects_negative():
    with pytest.raises(ValueError):
        Rectangle(-1, 2)


def test_circle_area():
    assert Circle(2).area() == pytest.approx(4 * math.pi)


def test_account_deposit_and_withdraw():
    acc = Account("Ann", 100)
    acc.deposit(50)
    acc.withdraw(30)
    assert acc.balance == 120


def test_account_rejects_overdraft():
    acc = Account("Ann", 10)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(50)
    assert acc.balance == 10


@pytest.mark.parametrize("amount", [0, -5])
def test_account_rejects_non_positive_amounts(amount):
    acc = Account("Ann", 10)
    with pytest.raises(ValueError):
        acc.deposit(amount)


def test_balance_is_read_only():
    acc = Account("Ann", 10)
    with pytest.raises(AttributeError):
        acc.balance = 1_000_000


def test_book_info():
    assert Book("Dune", "Frank Herbert", 412).info() == "'Dune' by Frank Herbert, 412 pages"


def test_movie_play(capsys):
    assert Movie("Up", "Pete Docter", 2009).play() == "Playing the movie Up..."
    assert "Playing the movie Up..." in capsys.readouterr().out
