from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    price: float


@dataclass
class Order:
    amount: float
    has_discount: bool
    region: str
    currency: str
    type: str
    items: list[Item] = field(default_factory=list)


@dataclass
class User:
    is_premium: bool
    is_admin: bool
    is_trial: bool
    region: str


def is_eligible_amount(order: Order, user: User) -> bool:
    return order.amount > 1000 or (order.type == "bulk" and not user.is_trial)


VALID_REGION_CURRENCY = {("EU", "EUR"): True, ("US", "USD"): True, ("JP", "YEN"): True}


def has_valid_currency(order: Order, user: User) -> bool:
    return VALID_REGION_CURRENCY.get((user.region, order.currency), False)


def approve_order(order: Order, user: User) -> str:
    # Guard clause: reject early
    if user.is_admin:
        return "approved"

    rejection_rules = [
        lambda: not user.is_premium,
        lambda: order.amount is None,
        lambda: not is_eligible_amount(order, user),
        lambda: order.has_discount,
        lambda: not has_valid_currency(order, user),
        lambda: any(item.price < 0 for item in order.items),
    ]

    if any(rule() for rule in rejection_rules):
        return "rejected"

    return "approved"


def main() -> None:
    user = User(
        is_premium=True,
        is_admin=False,
        is_trial=False,
        region="US",
    )

    order = Order(
        amount=1500,
        has_discount=False,
        region="EU",
        currency="USD",
        type="normal",
        items=[
            Item("Keyboard", 100.0),
            Item("Monitor", 200.0),
            Item("Mouse", 50.0),
        ],
    )

    result = approve_order(order, user)
    print(f"Order approval result: {result}")


if __name__ == "__main__":
    main()
