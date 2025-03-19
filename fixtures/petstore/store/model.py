import attr
from faker import Faker
from fixtures.base import BaseClass

fake = Faker()


@attr.s
class Order(BaseClass):
    """
    Represents an order for a pet.
    """

    id: int = attr.ib(default=fake.random_int(min=1, max=10000))
    petId: int = attr.ib(default=fake.random_int(min=1, max=10000))
    quantity: int = attr.ib(default=fake.random_int(min=1, max=10))
    shipDate: str = attr.ib(default=fake.iso8601())
    status: str = attr.ib(
        default=fake.random_element(elements=["placed", "approved", "delivered"])
    )
    complete: bool = attr.ib(default=fake.boolean())

    @staticmethod
    def random():
        return Order()

    def to_dict(self):
        return {
            "id": self.id,
            "petId": self.petId,
            "quantity": self.quantity,
            "shipDate": self.shipDate,
            "status": self.status,
            "complete": self.complete,
        }
