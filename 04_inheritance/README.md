# 04 · Inheritance (OOP exercises notebook 2, part 2)

| # | Exercise | Concepts |
|---|---|---|
| 1 | `Vehicle.drive()` overridden by `Car` and `Bicycle` | overriding, polymorphism |
| 2 | `Person.introduce()` with `Student` and `Employee` subclasses | `super().__init__`, overriding |
| 3 | `BankAccount` → `SavingsAccount` with interest, `check_balance` and `transfer` | reuse of parent methods via `super()` |

```mermaid
classDiagram
    Vehicle <|-- Car
    Vehicle <|-- Bicycle
    Vehicle : +drive() str
    Person <|-- Student
    Person <|-- Employee
    Person : +name +age +address +introduce() str
    Student : +field_of_study
    Employee : +company
    BankAccount <|-- SavingsAccount
    BankAccount : +account_number -_balance +deposit() +withdraw() +transfer(dest, amount) bool
    SavingsAccount : +interest_rate +add_interest() +check_balance()
```

`add_interest()` calls the parent's `deposit()` (as the exercise asks) instead of touching the balance directly, so every rule on deposits still applies.

Run: `pytest 04_inheritance`
