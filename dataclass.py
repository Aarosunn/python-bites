from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod


@dataclass(frozen=True, order=True, slots=True, kw_only=True)
class User:
    name: str
    email: str
    # 1. Default value
    active: bool = True
    tags: list[str] = field(default_factory=list[str])
    # 2. Derived fields
    slug: str = field(init=False)

    def __post_init__(self):
        normalized_name = self.name.strip().title()
        slugified = self.name.lower().replace(" ", "-")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "slug", slugified)

    # 3. Dataclasses are still classes

    @property
    def domain(self) -> str:
        return self.email.split("@")[-1]

    def contact_card(self) -> str:
        return f"{self.name} <{self.email}>"


# 4. Frozen dataclasses
# 5. Slots, Ordering, Keyword-only arguments

# 6. (did not do) Custom constructors @classmethod

# 8. Abstract Dataclasses


@dataclass
class Account(ABC):
    owner: str
    base_fee: float

    @property
    @abstractmethod
    def monthly_fee(self) -> float: ...


@dataclass
class FreeAccount(Account):
    @property
    def monthly_fee(self) -> float:
        return 0.0


@dataclass
class PremiumAccount(Account):
    extra_storage_gb: int = 100

    @property
    def monthly_fee(self) -> float:
        return self.base_fee + (self.extra_storage_gb * 0.10)


def main():
    u1 = User(name="alice smith", email="alice@example.com", active=False)
    u2 = User(name="bob", email="bob@example.com")
    print("u1: ", u1, u1.contact_card(), u1.domain)
    u2.tags.append("hi_tag")
    print("u2: ", u2)
    print(u1 < u2)
    print(asdict(u1))  # 7. Serialization Helpers

    free_account = FreeAccount(owner="Aaron", base_fee=10)
    premium_account = PremiumAccount(owner="Michael", base_fee=10, extra_storage_gb=50)
    print(premium_account, premium_account.monthly_fee)
    print(free_account, free_account.monthly_fee)

    # Ellipses literal
    # import numpy as np
    #
    # arr = np.zeros((3, 4, 5, 6))
    # print(arr)
    # print(arr[..., 0])


if __name__ == "__main__":
    main()
