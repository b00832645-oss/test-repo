import pytest
from operators import Complex, Person, Vector, Circle, Point2D, Matrix


def test_complex_add_sub():
    assert Complex(1, 2) + Complex(3, -5) == Complex(4, -3)
    assert Complex(1, 2) - Complex(3, -5) == Complex(-2, 7)


def test_complex_returns_new_object():
    a = Complex(1, 1)
    b = a + Complex(1, 1)
    assert a == Complex(1, 1) and b is not a


def test_complex_with_unsupported_type_raises_type_error():
    with pytest.raises(TypeError):
        Complex(1, 1) + 5


def test_person_gt_by_age():
    assert Person("Ann", 30, "F") > Person("Bob", 25, "M")
    assert not Person("Ann", 20, "F") > Person("Bob", 25, "M")


def test_vector_dot_product():
    assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32


@pytest.mark.parametrize("a, b, lt, eq", [(1, 2, True, False), (2, 2, False, True), (3, 2, False, False)])
def test_circle_all_comparisons(a, b, lt, eq):
    c1, c2 = Circle(a), Circle(b)
    assert (c1 < c2) is lt
    assert (c1 == c2) is eq
    assert (c1 != c2) is (not eq)
    assert (c1 <= c2) is (lt or eq)
    assert (c1 > c2) is (not lt and not eq)
    assert (c1 >= c2) is (not lt)


def test_sorted_uses_lt():
    assert [c.radius for c in sorted([Circle(3), Circle(1), Circle(2)])] == [1, 2, 3]


def test_point_comparison_by_distance():
    assert Point2D(3, 4) > Point2D(1, 1)
    assert Point2D(3, 4) == Point2D(0, 5)      # both at distance 5
    assert Point2D(0, 1) <= Point2D(1, 0)


def test_matrix_multiplication():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    assert a * b == Matrix([[19, 22], [43, 50]])
    assert a @ b == a * b


def test_matrix_non_square():
    assert Matrix([[1, 2, 3]]) * Matrix([[1], [2], [3]]) == Matrix([[14]])


def test_matrix_shape_mismatch():
    with pytest.raises(ValueError):
        Matrix([[1, 2]]) * Matrix([[1, 2]])
