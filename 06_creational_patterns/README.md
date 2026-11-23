# 06 · Creational patterns

Exercises from the course page *Creational patterns*: refactor three pieces of "spaghetti" code.

| Folder | Pattern | Legacy problem |
|---|---|---|
| [`01_factory_payment/`](01_factory_payment/) | Factory Method | `process_payment()` with one `if/elif` branch per payment method |
| [`02_builder_employee/`](02_builder_employee/) | Builder | `create_employee()` with 17 positional parameters |
| [`03_singleton_config/`](03_singleton_config/) | Singleton | `config.json` re-read by every module |

Each folder contains `legacy_*.py` (the starting code, kept for comparison), the refactored solution, tests and a UML diagram.
