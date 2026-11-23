# 09 · Testing with pytest

Exercises from the course page *Introduction to testing in Python*: test a small e-commerce app at every level of the testing pyramid, then mock an LLM API.

| File | What it shows |
|---|---|
| `shop.py` | Code under test: domain functions (discount, tax, total), `ProductRepository` and `OrderService` |
| `conftest.py` | Shared fixtures (fresh repository and service for each test) |
| `test_shop_unit.py` | **Unit tests:** one function at a time, `pytest.raises`, `parametrize`, `approx` |
| `test_shop_integration.py` | **Integration tests:** `OrderService` + a real `ProductRepository` working together |
| `test_shop_properties.py` | **Property-based tests** (Hypothesis): rules that must hold for any input |
| `groq_chat.py` / `test_groq_chat.py` | **Mocking:** a fake Groq client returns `"4"`, the exact API call is checked, and an outage is simulated |

Concepts covered:
- **AAA pattern:** every test is split into Arrange / Act / Assert.
- **Fixtures** in `conftest.py`, shared without imports.
- **Markers:** `@pytest.mark.slow` on the test that would call the real API. It's skipped unless `GROQ_API_KEY` is set and is deselected with `pytest -m "not slow"`.
- **Coverage:** `pytest --cov=shop --cov=groq_chat --cov-report=term-missing`.
- **Mocking rule:** mock what you don't own (the Groq API), test what you own (validation, the request you send, error handling). `ask_groq` takes the client as a parameter (dependency injection), which is what makes it mockable.

Run:
```bash
pytest 09_testing                     # everything (the real-API test is skipped)
pytest 09_testing -m "not slow"       # only fast tests
pytest 09_testing --cov=shop --cov=groq_chat --cov-report=term-missing
```
