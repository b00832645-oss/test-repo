# Hospital Management System

**Workflow:** a patient posts a health problem → the organizer reads it and consults a doctor → the doctor writes a prescription → the organizer sends it to the patient → the patient pays (check, cash or credit card) → the organizer forwards the payment to the doctor. The organizer is also the administrator: they maintain the database and issue member IDs and passwords.

## Task 1 & 2: class diagram (with the Task 3 additions)

```mermaid
classDiagram
    direction LR
    class User {
        <<abstract>>
        #id: int
        #name: str
        #password_hash: str
        +login(password: str) bool
        +logout()
    }
    class Patient {
        -address: str
        +submit_problem(description: str) HealthProblem
        +pay(prescription, method: PaymentMethod) Payment
    }
    class Doctor {
        -speciality: str
        -balance: float
        +write_prescription(problem, text, fee) Prescription
        +receive_payment(amount: float)
    }
    class Organizer {
        +register_member(user: User) int
        +assign(problem, doctor)
        +send_prescription(prescription)
        +forward_payment(payment)
    }
    class HealthProblem {
        -id: int
        -description: str
        -status: ProblemStatus
        -created_at: datetime
        +mark_in_review()
        +resolve()
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Prescription {
        -id: int
        -text: str
        -fee: float
        -issued_at: datetime
    }
    class Payment {
        -amount: float
        -paid_at: datetime
        -forwarded: bool
    }
    class PaymentMethod {
        <<abstract>>
        +process(amount: float) bool*
    }
    class CheckPayment { -check_number: str }
    class CashPayment
    class CreditCardPayment { -card_number: str }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" --> "0..*" HealthProblem : submits
    Organizer "1" --> "0..*" HealthProblem : manages
    HealthProblem "0..*" --> "0..1" Doctor : assigned to
    HealthProblem --> ProblemStatus
    HealthProblem "1" *-- "0..*" Prescription : answered by
    Doctor "1" --> "0..*" Prescription : writes
    Prescription "1" --> "0..1" Payment : settled by
    Payment --> "1" PaymentMethod : uses
    PaymentMethod <|-- CheckPayment
    PaymentMethod <|-- CashPayment
    PaymentMethod <|-- CreditCardPayment
```

Design choices:
- `User` superclass: id, name, password and login/logout are shared by every actor (Task 3).
- Payment types use **polymorphism**. `Payment` holds a `PaymentMethod`, and each subclass implements `process()`. This is the Strategy pattern.
- `HealthProblem ◆ Prescription` is a composition: a prescription has no meaning without the problem it answers, and the problem keeps the history of past prescriptions.
- Status tracking with an enumeration and timestamps on each event (Task 3).

## Task 2: sequence diagram, one patient from problem to payment

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    participant M as PaymentMethod
    P->>O: submit_problem("persistent cough")
    O->>O: status = IN_REVIEW
    O->>D: assign(problem)
    D-->>O: prescription (fee 40€)
    O->>P: send_prescription(prescription)
    P->>M: process(40)
    M-->>P: True
    P->>O: payment
    O->>D: forward_payment(40)
    O->>O: status = RESOLVED
```

## Task 3: system sequence diagrams

**Patient registration**
```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant DB as Database
    P->>O: request membership (name, address)
    O->>DB: create Patient
    DB-->>O: new member id
    O-->>P: member id + temporary password
    P->>O: login(id, password)
    O-->>P: authenticated
```

**Consultation flow**
```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>O: submit_problem(description)
    O-->>P: problem #id (PENDING)
    O->>O: mark_in_review()
    O->>D: assign(problem)
    D->>D: examine
    D-->>O: write_prescription(problem, text, fee)
    O-->>P: send_prescription(prescription)
```

**Payment processing**
```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant M as PaymentMethod
    participant D as Doctor
    P->>O: pay(prescription, method)
    O->>M: process(fee)
    alt payment accepted
        M-->>O: True
        O->>D: forward_payment(fee)
        O-->>P: receipt
    else payment refused
        M-->>O: False
        O-->>P: error, problem stays IN_REVIEW
    end
```

## HealthProblem lifecycle

```mermaid
stateDiagram-v2
    [*] --> PENDING : submitted
    PENDING --> IN_REVIEW : organizer assigns a doctor
    IN_REVIEW --> RESOLVED : prescription paid
    RESOLVED --> [*]
```

## Questions to consider

| Question | Answer |
|---|---|
| A patient consulting multiple doctors? | Each `HealthProblem` is assigned to one doctor, and a patient has `0..*` problems, so several doctors are reached through several problems. For a second opinion on the same problem, make the association `HealthProblem "0..*" -- "1..*" Doctor` or add a `Consultation` association class. |
| Reusable prescriptions? | Split a `Medication` / `Treatment` catalogue (reusable, aggregation) from the `Prescription` instance (composition with its problem, with dosage and date). Renewals reference the previous prescription. |
| Which pattern for payments? | **Strategy**: `PaymentMethod` is the strategy interface, Check/Cash/CreditCard are the concrete strategies, and `Payment` is the context. A **Factory** can create the method from the patient's choice. |
| Data integrity during payments? | Make payment + forwarding atomic (a database transaction), forward only after a successful `process()`, keep payments idempotent (one payment per prescription, checked with `forwarded` / a unique key) and log every step. |
