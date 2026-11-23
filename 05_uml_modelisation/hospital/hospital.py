"""Implementation of the Hospital Management System class diagram."""
from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from itertools import count


class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in-review"
    RESOLVED = "resolved"


class User(ABC):
    _ids = count(1)

    def __init__(self, name: str, password: str):
        self.id = next(User._ids)
        self.name = name
        self._password_hash = self._hash(password)
        self.logged_in = False

    @staticmethod
    def _hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, password: str) -> bool:
        self.logged_in = self._hash(password) == self._password_hash
        return self.logged_in

    def logout(self) -> None:
        self.logged_in = False


# --- payment strategies --------------------------------------------------------
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...


class CashPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        return amount > 0


class CheckPayment(PaymentMethod):
    def __init__(self, check_number: str):
        self.check_number = check_number

    def process(self, amount: float) -> bool:
        return amount > 0 and self.check_number.isdigit()


class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str):
        self._card_number = card_number

    def process(self, amount: float) -> bool:
        return amount > 0 and len(self._card_number) == 16 and self._card_number.isdigit()


# --- domain objects -------------------------------------------------------------
class Prescription:
    def __init__(self, problem: "HealthProblem", doctor: "Doctor", text: str, fee: float):
        self.problem = problem
        self.doctor = doctor
        self.text = text
        self.fee = fee
        self.issued_at = datetime.now()
        self.payment: Payment | None = None


class Payment:
    def __init__(self, prescription: Prescription, method: PaymentMethod):
        self.prescription = prescription
        self.method = method
        self.amount = prescription.fee
        self.paid_at = datetime.now()
        self.forwarded = False


class HealthProblem:
    _ids = count(1)

    def __init__(self, patient: "Patient", description: str):
        self.id = next(HealthProblem._ids)
        self.patient = patient
        self.description = description
        self.status = ProblemStatus.PENDING
        self.created_at = datetime.now()
        self.doctor: Doctor | None = None
        self.prescriptions: list[Prescription] = []   # history (composition)

    def mark_in_review(self, doctor: "Doctor") -> None:
        self.doctor = doctor
        self.status = ProblemStatus.IN_REVIEW

    def resolve(self) -> None:
        self.status = ProblemStatus.RESOLVED


class Patient(User):
    def __init__(self, name: str, password: str, address: str = ""):
        super().__init__(name, password)
        self.address = address
        self.problems: list[HealthProblem] = []
        self.inbox: list[Prescription] = []

    def submit_problem(self, description: str) -> HealthProblem:
        problem = HealthProblem(self, description)
        self.problems.append(problem)
        return problem

    def pay(self, prescription: Prescription, method: PaymentMethod) -> Payment:
        if prescription.payment is not None:
            raise ValueError("Prescription already paid")
        if not method.process(prescription.fee):
            raise ValueError("Payment refused")
        prescription.payment = Payment(prescription, method)
        return prescription.payment


class Doctor(User):
    def __init__(self, name: str, password: str, speciality: str):
        super().__init__(name, password)
        self.speciality = speciality
        self.balance = 0.0

    def write_prescription(self, problem: HealthProblem, text: str, fee: float) -> Prescription:
        if problem.doctor is not self:
            raise PermissionError("This problem is not assigned to you")
        prescription = Prescription(problem, self, text, fee)
        problem.prescriptions.append(prescription)
        return prescription

    def receive_payment(self, amount: float) -> None:
        self.balance += amount


class Organizer(User):
    def __init__(self, name: str, password: str):
        super().__init__(name, password)
        self.members: dict[int, User] = {}

    def register_member(self, user: User) -> int:
        self.members[user.id] = user
        return user.id

    def assign(self, problem: HealthProblem, doctor: Doctor) -> None:
        if problem.status is not ProblemStatus.PENDING:
            raise ValueError("Only pending problems can be assigned")
        problem.mark_in_review(doctor)

    def send_prescription(self, prescription: Prescription) -> None:
        prescription.problem.patient.inbox.append(prescription)

    def forward_payment(self, payment: Payment) -> None:
        if payment.forwarded:
            raise ValueError("Payment already forwarded")      # idempotence
        payment.prescription.doctor.receive_payment(payment.amount)
        payment.forwarded = True
        payment.prescription.problem.resolve()


if __name__ == "__main__":
    org = Organizer("Olivia", "admin")
    pat = Patient("Paul", "pw", "Paris")
    doc = Doctor("Dr Diane", "pw", "GP")
    for u in (pat, doc):
        org.register_member(u)
    problem = pat.submit_problem("persistent cough")
    org.assign(problem, doc)
    rx = doc.write_prescription(problem, "Rest + syrup 3x/day", fee=40)
    org.send_prescription(rx)
    payment = pat.pay(rx, CreditCardPayment("4242424242424242"))
    org.forward_payment(payment)
    print(problem.status, doc.balance)
