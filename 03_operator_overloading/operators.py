"""OOP exercises notebook 2, part 1: operator overloading."""
from __future__ import annotations

import math
from functools import total_ordering


# 1. Complex numbers -----------------------------------------------------------
class Complex:
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return (self.real, self.imag) == (other.real, other.imag)

    def __hash__(self):
        return hash((self.real, self.imag))

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"({self.real} {sign} {abs(self.imag)}i)"


# 2. Person compared by age ------------------------------------------------------
class Person:
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age})"


# 4. Vector dot product ----------------------------------------------------------
class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __mul__(self, other):
        """vector1 * vector2 -> dot product (a number)."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# 5. Circles compared by radius (all six operators) -------------------------------
@total_ordering                     # generates <=, >, >= from __eq__ and __lt__
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __hash__(self):
        return hash(self.radius)

    def __repr__(self):
        return f"Circle({self.radius})"


# 6. 2D points compared by Euclidean distance to the origin -----------------------
@total_ordering
class Point2D:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def distance(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        return math.isclose(self.distance(), other.distance())

    def __lt__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance() < other.distance() and not self == other

    __hash__ = None   # equal distances != same point: not safe as dict keys

    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"


# 7. Matrix multiplication -------------------------------------------------------
class Matrix:
    def __init__(self, rows: list[list[float]]):
        if not rows or any(len(r) != len(rows[0]) for r in rows):
            raise ValueError("All rows must be non-empty and have the same length")
        self.rows = [list(r) for r in rows]

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        (n, m), (m2, p) = self.shape, other.shape
        if m != m2:
            raise ValueError(f"Cannot multiply {n}x{m} by {m2}x{p}")
        return Matrix([[sum(self.rows[i][k] * other.rows[k][j] for k in range(m))
                        for j in range(p)] for i in range(n)])

    __matmul__ = __mul__      # also support the standard A @ B syntax

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    __hash__ = None           # mutable container

    def __repr__(self):
        return f"Matrix({self.rows})"


if __name__ == "__main__":
    print(Complex(1, 2) + Complex(3, -5), Complex(1, 2) - Complex(3, -5))
    print(Person("Ann", 30, "F") > Person("Bob", 25, "M"))
    print(Vector(1, 2, 3) * Vector(4, 5, 6))
    print(sorted([Circle(3), Circle(1), Circle(2)]))
    print(Point2D(3, 4) > Point2D(1, 1))
    print(Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]]))
