"""Decorator pattern refactoring of the order pricing system."""
from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float: ...

    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def get_base_price(self) -> float: ...


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        if base_price < 0:
            raise ValueError("Base price cannot be negative")
        self._price = base_price

    def get_cost(self) -> float:
        return self._price

    def get_description(self) -> str:
        return f"Base price: {self._price:.2f}€"

    def get_base_price(self) -> float:
        return self._price


class OrderDecorator(OrderComponent):
    """Base decorator: delegates everything to the wrapped order."""

    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()

    def get_base_price(self) -> float:
        return self._order.get_base_price()


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def get_cost(self):
        return self._order.get_cost() + self.COST

    def get_description(self):
        return self._order.get_description() + f"\nExpress shipping: +{self.COST:.2f}€"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05                      # 5 % of the base price (legacy rule)

    def _amount(self):
        return self.get_base_price() * self.RATE

    def get_cost(self):
        return self._order.get_cost() + self._amount()

    def get_description(self):
        return self._order.get_description() + f"\nInsurance (5%): +{self._amount():.2f}€"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self):
        return self._order.get_cost() + self.COST

    def get_description(self):
        return self._order.get_description() + f"\nGift wrap: +{self.COST:.2f}€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        super().__init__(order)
        self.percent = percent

    def get_cost(self):
        return self._order.get_cost() * (1 - self.percent / 100)

    def get_description(self):
        saved = self._order.get_cost() * self.percent / 100
        return self._order.get_description() + f"\nDiscount ({self.percent}%): -{saved:.2f}€"


class PremiumMemberDecorator(OrderDecorator):
    RATE = 0.10

    def get_cost(self):
        return self._order.get_cost() * (1 - self.RATE)

    def get_description(self):
        saved = self._order.get_cost() * self.RATE
        return self._order.get_description() + f"\nPremium member (10%): -{saved:.2f}€"


if __name__ == "__main__":
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")
