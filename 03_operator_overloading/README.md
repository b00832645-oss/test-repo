# 03 · Operator overloading (OOP exercises notebook 2, part 1)

Make custom classes work with Python operators through special ("dunder") methods.

| # | Exercise | Operators | Dunder methods |
|---|---|---|---|
| 1 | Complex numbers | `+`, `-` | `__add__`, `__sub__` |
| 2 | Compare people by age | `>` | `__gt__` |
| 3 | *(not in the notebook)* | | |
| 4 | Vector dot product | `*` | `__mul__` |
| 5 | Compare circles by radius | `<` `>` `==` `!=` `>=` `<=` | `functools.total_ordering` + `__eq__`, `__lt__` |
| 6 | Compare 2D points by distance to the origin | all comparisons | same |
| 7 | Matrix multiplication | `*` (and `@`) | `__mul__`, `__matmul__` |

Key rules applied:
- Arithmetic operators return a new object and never modify `self`.
- They return `NotImplemented` for unsupported types, so Python can try the reflected method or raise a clean `TypeError`.
- Defining `__eq__` removes the default `__hash__`, so the immutable-looking classes define `__hash__` consistently with `__eq__`.

Run: `pytest 03_operator_overloading`
