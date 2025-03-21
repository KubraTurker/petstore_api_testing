import attr
from faker import Faker
from fixtures.base import BaseClass

fake = Faker()


@attr.s
class User(BaseClass):
    """
    Represents a user in the system.
    """

    id: int = attr.ib(default=fake.random_int(min=1, max=1000))
    username: str = attr.ib(default=fake.user_name())
    firstName: str = attr.ib(default=fake.first_name())
    lastName: str = attr.ib(default=fake.last_name())
    email: str = attr.ib(default=fake.email())
    password: str = attr.ib(default=fake.password())
    phone: str = attr.ib(default=fake.phone_number())
    userStatus: int = attr.ib(default=fake.random_int(min=0, max=1))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "userStatus": self.userStatus,
        }

    @staticmethod
    def random():
        return User()
