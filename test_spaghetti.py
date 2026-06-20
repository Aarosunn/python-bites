from spaghetti import Item, Order, User, approve_order
from typing import Any


def make_order(**kwargs):
    defaults: dict[str, Any] = dict(
        amount=1200,
        has_discount=False,
        region="US",
        currency="USD",
        type="normal",
        items=[Item("Keyboard", 100.0), Item("Mouse", 50.0)],
    )
    defaults.update(kwargs)
    return Order(**defaults)


def make_user(**kwargs):
    defaults: dict[str, Any] = dict(
        is_premium=False, is_admin=False, is_trial=False, region="US"
    )
    defaults.update(kwargs)
    return User(**defaults)


# --- Premium user scenarios --------------------


def test_premium_high_value_no_discount_non_eu():
    user = make_user(is_premium=True)
    order = make_order(amount=1500, region="US", currency="USD", has_discount=False)
    assert approve_order(order, user) == "approved"


def test_premium_high_value_no_discount_eu_eur():
    user = make_user(is_premium=True, region="EU")
    order = make_order(amount=1500, region="EU", currency="EUR", has_discount=False)
    assert approve_order(order, user) == "approved"


def test_premium_high_value_no_discount_eu_usd():
    user = make_user(is_premium=True, region="EU")
    order = make_order(amount=1500, region="EU", currency="USD", has_discount=False)
    assert approve_order(order, user) == "rejected"


def test_premium_high_value_with_discount():
    user = make_user(is_premium=True)
    order = make_order(amount=1500, has_discount=True)
    assert approve_order(order, user) == "rejected"


def test_premium_low_value_bulk_order_non_trial():
    user = make_user(is_premium=True)
    order = make_order(amount=900, type="bulk")
    assert approve_order(order, user) == "approved"


def test_premium_low_value_bulk_order_trial():
    user = make_user(is_premium=True, is_trial=True)
    order = make_order(amount=900, type="bulk")
    assert approve_order(order, user) == "rejected"


def test_premium_low_value_no_bulk_order():
    user = make_user(is_premium=True)
    order = make_order(amount=900)
    assert approve_order(order, user) == "rejected"


# -- Admin user scenarios -------------------


def test__admin():
    user = make_user(is_admin=True)
    order = make_order(amount=100, has_discount=True)
    assert approve_order(order, user) == "approved"


def test_admin_with_negative_item():
    user = make_user(is_admin=True)
    order = make_order(items=[Item("Something", -5)])
    assert approve_order(order, user) == "approved"


def test_non_premium_non_admin():
    user = make_user()
    order = make_order()
    assert approve_order(order, user) == "rejected"


# --- Regular user scenarios ---------------------


def test_regular_user_rejected_even_if_high_value():
    user = make_user()
    order = make_order(amount=2000)
    assert approve_order(order, user) == "rejected"


def test_regular_user_with_disount():
    user = make_user()
    order = make_order(has_discount=True)
    assert approve_order(order, user) == "rejected"


# --- Exception handling --------------------


def test_invalid_order_raises_exception_is_caught():
    user = make_user(is_premium=True)
    broken_order = make_order(amount=None)
    assert approve_order(broken_order, user) == "rejected"
