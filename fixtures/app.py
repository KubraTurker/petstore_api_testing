from fixtures.petstore.store.api import StoreAPI
from fixtures.petstore.user.api import UserAPI
from fixtures.requests import Client
from fixtures.petstore.pet.api import PetAPI


class Application:

    def __init__(self, url):
        self.url = url

        self.client = Client

        self.pet_api = PetAPI(self)
        self.store_api = StoreAPI(self)
        self.user_api = UserAPI(self)
