"""OOP exercises notebook 1: five basic classes."""
import math


class Rectangle:
    def __init__(self, width: float, height: float):
        if width < 0 or height < 0:
            raise ValueError("Width and height must be non-negative")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Circle:
    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def __repr__(self):
        return f"Circle(radius={self.radius})"


class Account:
    """Bank account: the balance can only change through deposit/withdraw."""

    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance

    def __repr__(self):
        return f"Account(owner={self.owner!r}, balance={self._balance})"


class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    def info(self) -> str:
        return f"'{self.title}' by {self.author}, {self.pages} pages"


class Movie:
    def __init__(self, title: str, director: str, year: int):
        self.title = title
        self.director = director
        self.year = year

    def play(self) -> str:
        message = f"Playing the movie {self.title}..."
        print(message)
        return message


if __name__ == "__main__":
    print(Rectangle(3, 4).area())
    print(round(Circle(1).area(), 2))
    acc = Account("Louis", 100)
    acc.deposit(50)
    acc.withdraw(30)
    print(acc)
    print(Book("Clean Code", "Robert C. Martin", 464).info())
    Movie("Inception", "Christopher Nolan", 2010).play()
