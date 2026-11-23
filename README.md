# OOP & Design Patterns in Python: course exercises

Solutions to the practical exercises of the **Object-Oriented Programming & Design Patterns in Python** module (AIDAMS 2A, CentraleSupélec × ESSEC), taken from the course slides and [courses.dallard.tech](https://courses.dallard.tech/).

Every exercise folder contains a `README.md` (the problem, the design decisions and a UML diagram that GitHub renders), the solution code and **pytest** tests.

![tests](../../actions/workflows/tests.yml/badge.svg)

## Contents

| # | Folder | Topic | Source |
|---|---|---|---|
| 01 | [`01_git_workflow`](01_git_workflow/) | Git workflow (11 steps) + a dev-environment install script | slides: *Your first git workflow* |
| 02 | [`02_oop_basics`](02_oop_basics/) | Classes, attributes, methods, `@property` | OOP exercises notebook 1 |
| 03 | [`03_operator_overloading`](03_operator_overloading/) | Dunder methods: `+ - * @ < > ==`… | OOP exercises notebook 2 |
| 04 | [`04_inheritance`](04_inheritance/) | Inheritance, overriding, `super()` | OOP exercises notebook 2 |
| 05 | [`05_uml_modelisation`](05_uml_modelisation/) | UML: Hospital Management System, ABCD Records (diagrams + implementation) | slides: *Practice UML exo* |
| 06 | [`06_creational_patterns`](06_creational_patterns/) | Factory Method · Builder · Singleton | course page *Creational patterns* |
| 07 | [`07_structural_patterns`](07_structural_patterns/) | Adapter · Decorator | course page *Structural patterns* |
| 08 | [`08_behavioral_patterns`](08_behavioral_patterns/) | Strategy · Template Method | course page *Behavioral patterns* |
| 09 | [`09_testing`](09_testing/) | Unit, integration and property-based tests; fixtures; mocking an LLM API; markers; coverage | course page *Introduction to testing in Python* |
| 10 | [`10_fastapi_rest_api`](10_fastapi_rest_api/) | REST API with FastAPI: layered architecture, dependency injection, a small event bus | slides: *FastAPI example*, *REST APIs with FastAPI* |

## Setup

```bash
git clone https://github.com/<your-username>/oop-aidams-exercises.git
cd oop-aidams-exercises
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                                  # runs every exercise's tests
```

Or run `./01_git_workflow/scripts/install_dev_env.sh` to do all of the above.

Useful commands:
```bash
pytest 06_creational_patterns            # one chapter
pytest -m "not slow"                     # skip slow tests
pytest --cov=. --cov-report=term-missing # coverage
python 06_creational_patterns/01_factory_payment/payment_factory.py   # run a demo
```

Each design-pattern folder keeps the original "spaghetti" code as `legacy_*.py`, so the before/after comparison is visible. Where possible, the tests check that the refactored code gives exactly the same results as the legacy code.

## Course principles applied throughout
- Draw the UML **before** coding (every folder starts with its diagram).
- Program to interfaces: abstract base classes (`abc.ABC`) with small, focused contracts.
- Prefer composition over inheritance; `@property` for encapsulation; `@classmethod` for factory methods.
- Respect SOLID, especially **Open/Closed**: new behaviour = a new class, not an edited `if/elif`.
- Tests follow the **Arrange-Act-Assert** pattern; mock what you don't own.
