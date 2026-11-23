# ABCD Records

A mail-order company sells CDs and tapes at discount prices to record-club members.
- Only members can order; non-members receive a membership application form.
- Two member classes: **Royal** (discount + priority, can order unavailable items) and **Regular**.
- Payment by cash, check or bank draft.
- The Order Processing Clerk verifies and processes orders; the Collection Department Clerk handles payments.
- All orders are saved to a daily records file.

## Level 1 + 2: use case diagram

```mermaid
flowchart LR
    M(["🧍 Member"])
    R(["🧍 Royal Member"])
    N(["🧍 Non-Member"])
    OPC(["🧍 Order Processing Clerk"])
    CDC(["🧍 Collection Dept Clerk"])
    R -- is a --> M

    subgraph ABCD["ABCD Records system"]
        PO([Place Order])
        VM([Verify Membership])
        VIA([Verify Item Availability])
        PRO([Process Order])
        AD([Apply Discount])
        OUI([Order Unavailable Items])
        PI([Print Invoice])
        PSL([Print Shipping List])
        MP([Make Payment])
        SMA([Send Membership Application])
    end

    M --- PO
    R --- OUI
    N --- SMA
    OPC --- VM
    OPC --- PRO
    CDC --- MP

    PO -. "«include»" .-> VM
    PRO -. "«include»" .-> VIA
    PRO -. "«include»" .-> PI
    PRO -. "«include»" .-> PSL
    AD -. "«extend»" .-> PRO
    OUI -. "«extend»" .-> PO
    SMA -. "«extend»" .-> VM
```

- `«include»` (mandatory): placing an order always verifies membership; processing always checks availability and prints the invoice and shipping list.
- `«extend»` (optional): a discount is applied only for Royal members; ordering unavailable items only for Royal members; the application form is sent only when verification fails (non-member).

## Level 1 + 2: class diagram

```mermaid
classDiagram
    direction LR
    class Member {
        <<abstract>>
        -member_id: str
        -name: str
        -address: str
        +discount_rate() float*
        +can_order_unavailable() bool*
        +place_order(lines) Order
    }
    class RoyalMember { +discount_rate() 0.10 +can_order_unavailable() True }
    class RegularMember { +discount_rate() 0.0 +can_order_unavailable() False }
    class Order {
        -order_id: int
        -date: date
        -status: str
        +total() float
    }
    class OrderLine { -quantity: int +subtotal() float }
    class Item {
        <<abstract>>
        -code: str
        -title: str
        -price: float
        -stock: int
        +is_available(qty) bool
    }
    class CD { -tracks: int }
    class Tape { -length_min: int }
    class Invoice { -amount: float +print() str }
    class ShippingList { -address: str +print() str }
    class Payment {
        <<abstract>>
        -amount: float
        +process() bool*
    }
    class CashPayment
    class CheckPayment { -check_number: str }
    class BankDraftPayment { -draft_number: str }
    class MembershipApplication { -name: str -address: str }
    class OrderProcessingClerk { +verify_membership(id) bool +process(order) }
    class CollectionClerk { +collect(order, payment) bool }
    class DailyRecords { +save(order) }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- CashPayment
    Payment <|-- CheckPayment
    Payment <|-- BankDraftPayment
    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine
    OrderLine "0..*" --> "1" Item
    Order "1" *-- "0..1" Invoice
    Order "1" *-- "0..1" ShippingList
    Order "1" --> "0..1" Payment
    OrderProcessingClerk ..> Order : processes
    CollectionClerk ..> Payment : handles
    DailyRecords o-- "0..*" Order
    OrderProcessingClerk ..> MembershipApplication : sends to non-members
```

## Level 2 scenario: a Royal member orders 2 CDs (one unavailable) and pays by check

```mermaid
sequenceDiagram
    actor RM as Royal Member
    participant OPC as Order Processing Clerk
    participant ORD as Order
    participant CD1 as CD (in stock)
    participant CD2 as CD (out of stock)
    participant CC as Collection Clerk
    participant DR as Daily Records
    RM->>OPC: place_order([CD1, CD2])
    OPC->>OPC: verify_membership(id) ✓ Royal
    OPC->>CD1: is_available(1)
    CD1-->>OPC: True
    OPC->>CD2: is_available(1)
    CD2-->>OPC: False
    Note over OPC,CD2: Royal members may order unavailable items → back-order
    OPC->>ORD: create(lines, discount 10%)
    OPC->>ORD: print invoice + shipping list (CD1 now, CD2 back-ordered)
    RM->>CC: pay(CheckPayment)
    CC->>CC: process() ✓
    CC->>DR: save(order)
```

## Level 3: sequence diagrams

**Membership verification (success and failure)**
```mermaid
sequenceDiagram
    actor U as Customer
    participant OPC as Order Processing Clerk
    participant DB as Member records
    U->>OPC: place_order(member_id, lines)
    OPC->>DB: find(member_id)
    alt member found
        DB-->>OPC: Member
        OPC-->>U: order accepted for processing
    else not a member
        DB-->>OPC: None
        OPC-->>U: MembershipApplication form
    end
```

**Payment processing (all types)**
```mermaid
sequenceDiagram
    actor M as Member
    participant CC as Collection Clerk
    participant P as Payment (Cash / Check / BankDraft)
    participant DR as Daily Records
    M->>CC: pay(order, payment)
    CC->>P: process()
    alt accepted
        P-->>CC: True
        CC->>DR: save(order, status = PAID)
        CC-->>M: receipt
    else refused (bad check / draft)
        P-->>CC: False
        CC-->>M: payment refused, order on hold
    end
```

**Item reordering for Royal members**
```mermaid
sequenceDiagram
    participant OPC as Order Processing Clerk
    participant I as Item
    participant S as Supplier
    actor RM as Royal Member
    OPC->>I: is_available(qty)
    I-->>OPC: False
    OPC->>OPC: can_order_unavailable()? Royal ✓
    OPC->>S: reorder(item, qty)
    S-->>OPC: delivery date
    OPC-->>RM: back-order confirmed (priority)
```
