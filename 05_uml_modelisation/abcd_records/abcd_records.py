"""Implementation of the ABCD Records class diagram."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from itertools import count


# --- items ----------------------------------------------------------------------
class Item(ABC):
    def __init__(self, code: str, title: str, price: float, stock: int):
        self.code, self.title, self.price, self.stock = code, title, price, stock

    def is_available(self, qty: int = 1) -> bool:
        return self.stock >= qty


class CD(Item):
    def __init__(self, code, title, price, stock, tracks: int = 12):
        super().__init__(code, title, price, stock)
        self.tracks = tracks


class Tape(Item):
    def __init__(self, code, title, price, stock, length_min: int = 60):
        super().__init__(code, title, price, stock)
        self.length_min = length_min


# --- members ----------------------------------------------------------------------
class Member(ABC):
    def __init__(self, member_id: str, name: str, address: str):
        self.member_id, self.name, self.address = member_id, name, address

    @abstractmethod
    def discount_rate(self) -> float: ...

    @abstractmethod
    def can_order_unavailable(self) -> bool: ...


class RoyalMember(Member):
    def discount_rate(self) -> float:
        return 0.10

    def can_order_unavailable(self) -> bool:
        return True


class RegularMember(Member):
    def discount_rate(self) -> float:
        return 0.0

    def can_order_unavailable(self) -> bool:
        return False


class MembershipApplication:
    def __init__(self, name: str = "", address: str = ""):
        self.name, self.address = name, address


# --- payments (Strategy) ----------------------------------------------------------
class Payment(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...


class CashPayment(Payment):
    def process(self, amount: float) -> bool:
        return amount > 0


class CheckPayment(Payment):
    def __init__(self, check_number: str):
        self.check_number = check_number

    def process(self, amount: float) -> bool:
        return amount > 0 and self.check_number.isdigit()


class BankDraftPayment(Payment):
    def __init__(self, draft_number: str):
        self.draft_number = draft_number

    def process(self, amount: float) -> bool:
        return amount > 0 and self.draft_number.startswith("BD")


# --- orders -------------------------------------------------------------------------
class OrderLine:
    def __init__(self, item: Item, quantity: int):
        self.item, self.quantity = item, quantity
        self.back_ordered = False

    def subtotal(self) -> float:
        return self.item.price * self.quantity


class Order:
    _ids = count(1)

    def __init__(self, member: Member):
        self.order_id = next(Order._ids)
        self.member = member
        self.date = date.today()
        self.lines: list[OrderLine] = []          # composition
        self.status = "created"

    def add_line(self, item: Item, quantity: int = 1) -> OrderLine:
        line = OrderLine(item, quantity)
        self.lines.append(line)
        return line

    def total(self) -> float:
        gross = sum(line.subtotal() for line in self.lines)
        return round(gross * (1 - self.member.discount_rate()), 2)

    def invoice(self) -> str:
        return f"Invoice #{self.order_id} for {self.member.name}: {self.total():.2f} €"

    def shipping_list(self) -> list[str]:
        return [f"{l.quantity} x {l.item.title}" for l in self.lines if not l.back_ordered]


class DailyRecords:
    def __init__(self):
        self.orders: list[Order] = []             # aggregation

    def save(self, order: Order) -> None:
        self.orders.append(order)


class OrderProcessingClerk:
    def __init__(self, members: dict[str, Member]):
        self.members = members

    def verify_membership(self, member_id: str) -> Member | MembershipApplication:
        return self.members.get(member_id) or MembershipApplication()

    def process(self, member_id: str, requests: list[tuple[Item, int]]) -> Order | MembershipApplication:
        member = self.verify_membership(member_id)
        if isinstance(member, MembershipApplication):
            return member                          # non-member gets the form
        order = Order(member)
        for item, qty in requests:
            if item.is_available(qty):
                item.stock -= qty
                order.add_line(item, qty)
            elif member.can_order_unavailable():
                order.add_line(item, qty).back_ordered = True
            else:
                raise ValueError(f"{item.title} is unavailable")
        order.status = "processed"
        return order


class CollectionClerk:
    def __init__(self, records: DailyRecords):
        self.records = records

    def collect(self, order: Order, payment: Payment) -> bool:
        if not payment.process(order.total()):
            order.status = "on hold"
            return False
        order.status = "paid"
        self.records.save(order)
        return True


if __name__ == "__main__":
    royal = RoyalMember("R1", "Rita", "Paris")
    opc = OrderProcessingClerk({"R1": royal})
    in_stock, out_of_stock = CD("C1", "Kind of Blue", 15, 3), CD("C2", "Blue Train", 12, 0)
    order = opc.process("R1", [(in_stock, 1), (out_of_stock, 1)])
    records = DailyRecords()
    print(order.invoice(), order.shipping_list())
    print(CollectionClerk(records).collect(order, CheckPayment("004512")), order.status)
