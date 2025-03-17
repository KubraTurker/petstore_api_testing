import attr
from faker import Faker
from fixtures.base import BaseClass

fake = Faker()


@attr.s
class Category(BaseClass):
    id: int = attr.ib(default=fake.random_int(min=1, max=1000))
    name: str = attr.ib(default=fake.word())

    def to_dict(self):
        return {"id": self.id, "name": self.name}


@attr.s
class Pet(BaseClass):
    id: int = attr.ib(default=None)
    category: Category = attr.ib(default=Category())
    name: str = attr.ib(default=fake.first_name())
    photoUrls: list = attr.ib(default=[fake.image_url()])
    tags: list = attr.ib(default=[])
    status: str = attr.ib(
        default=fake.random_element(elements=["available", "pending", "sold"])
    )

    @staticmethod
    def random():
        return Pet()

    def to_dict(self):
        return {
            "id": self.id,
            "category": (
                self.category.to_dict()
                if isinstance(self.category, Category)
                else self.category
            ),
            "name": self.name,
            "photoUrls": self.photoUrls,
            "tags": self.tags,
            "status": self.status,
        }


@attr.s
class ApiResponse(BaseClass):
    code: int = attr.ib()
    type: str = attr.ib()
    message: str = attr.ib()
    id: int = attr.ib(default=None)
    name: str = attr.ib(default=None)
    category: str = attr.ib(default=None)

    def to_dict(self):
        return {
            "code": self.code,
            "type": self.type,
            "message": self.message,
            "id": self.id,
            "name": self.name,
            "category": self.category,
        }
