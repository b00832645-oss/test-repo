"""OOP exercises notebook 2, part 2: inheritance."""


# 1. Vehicles -------------------------------------------------------------------
class Vehicle:
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


# 2. People ---------------------------------------------------------------------
class Person:
    def __init__(self, name: str, age: int, address: str):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, {self.age} years old, living at {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study: str):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        return f"Hi, I'm {self.name} and I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company: str):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return f"Hi, I'm {self.name} and I work at {self.company}."


# 3. Bank accounts --------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0):
        self.account_number = account_number
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def transfer(self, destination_account: "BankAccount", amount: float) -> bool:
        """Move money to another account. False if the balance is insufficient."""
        if not self.withdraw(amount):
            return False
        destination_account.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, balance: float = 0.0, interest_rate: float = 0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self) -> float:
        interest = round(self.balance * self.interest_rate, 2)
        if interest > 0:
            super().deposit(interest)        # reuse the parent's rules
        return interest

    def check_balance(self) -> float:
        return self.balance


if __name__ == "__main__":
    for v in [Vehicle(), Car(), Bicycle()]:
        print(v.drive())                       # polymorphism
    for p in [Student("Ann", 20, "Paris", "AI"), Employee("Bob", 35, "Lyon", "EDF")]:
        print(p.introduce())
    a, b = SavingsAccount("FR-001", 1000, 0.05), SavingsAccount("FR-002", 200)
    print(a.transfer(b, 300), a.check_balance(), b.check_balance())
    print(b.transfer(a, 10_000))
    print(a.add_interest(), a.check_balance())
