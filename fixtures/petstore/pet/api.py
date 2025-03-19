from requests import Response
from common.deco import logging as log
from fixtures.petstore.pet.model import Pet
from fixtures.validator import Validator


class PetAPI(Validator):

    def __init__(self, app):
        """
        PetAPI class provides helper methods for pet-related API operations.
        :param app: Application object that provides the client for making API requests.
        """
        self.app = app

    POST_PET = "/pet"  # Endpoint used to add a pet
    GET_PET = "/pet/{}"  # Endpoint used to retrieve a pet
    PUT_PET = "/pet"  # Endpoint used to update a pet
    DELETE_PET = "/pet/{}"  # Endpoint used to delete a pet

    @log("Adding a new pet")
    def add_pet(self, data: Pet, type_response=Pet) -> Response:
        """
        Adds a new pet.
        :param data: An object from the Pet model. This contains the data of the pet to be added.
        :param type_response: (optional) Determines which type to convert the response to (Pet by default).
        :return: Response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_PET}",
            json=data.to_dict(),  # Send pet data in JSON format
        )
        return self.structure(
            response, type_response=type_response
        )  # Structure the response

    @log("Retrieving pet by ID")
    def get_by_id_pet(self, pet_id: int, type_response=Pet) -> Response:
        """
        Retrieves a pet with the given ID.
        :param pet_id: Unique identifier (ID) of the pet.
        :param type_response: (optional) Determines which type to convert the response to (Pet by default).
        :return: Response containing the pet's information.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_PET.format(pet_id)}",  # Pet ID is added to the URL
        )
        return self.structure(
            response, type_response=type_response
        )  # Structure the response

    @log("Updating an existing pet")
    def update_pet(self, data: Pet, type_response=Pet) -> Response:
        """
        Updates an existing pet.
        :param data: An object from the Pet model. This contains the updated pet data.
        :param type_response: (optional) Determines which type to convert the response to (Pet by default).
        :return: Response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="PUT",
            url=f"{self.app.url}{self.PUT_PET}",
            json=data.to_dict(),  # Send updated pet data in JSON format
        )
        return self.structure(
            response, type_response=type_response
        )  # Structure the response

    @log("Deleting pet by ID")
    def delete_pet(self, pet_id: int) -> Response:
        """
        Deletes a specific pet by pet ID.
        :param pet_id: Unique identifier (ID) of the pet to be deleted.
        :return: Response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_PET.format(pet_id)}",  # Pet ID is added to the URL
        )
        return response  # Return the response related to the deletion operation
