import time
import logging
import pytest

from fixtures.petstore.pet.model import Pet, ApiResponse, Category


class TestPet:

    @pytest.mark.positive
    def test_add_pet(self, app):
        """
        Test for adding a new pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Assert that the status code is 200 (or 201).
            4. Assert that the response contains the pet ID and name.
        """
        data = Pet.random()

        res = app.pet_api.add_pet(data=data, type_response=Pet)

        assert res.status_code == 200
        assert isinstance(res.data, Pet), "Response data is not a Pet object"
        assert res.data.name == data.name, "Pet name mismatch"

    @pytest.mark.negative
    def test_add_pet_with_invalid_status(self, app):
        """
        Test for adding a pet with invalid status.
        Steps:
            1. Create a pet object with invalid status.
            2. Attempt to add the pet to the store.
            3. Assert that the status code is 400 or 500 (error).
            4. Verify the API rejects invalid status values.
        """
        data = Pet(
            name="InvalidStatusPet",
            category=Category(id=1, name="Test Category"),
            photoUrls=["https://example.com/pet-photo.jpg"],
            tags=["test", "invalid"],
            status="invalid_status",
        )

        response = app.pet_api.add_pet(data=data, type_response=ApiResponse)

        assert response.status_code in [
            400,
            500,
        ], f"Expected: 400 or 500, Received: {response.status_code}"

    @pytest.mark.positive
    def test_get_pet_by_id(self, app):
        """
        Test for retrieving a pet by ID.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Retrieve the pet by its ID.
            4. Assert that the response status code is 200.
            5. Assert that the retrieved pet has the same ID and name.
        """
        data = Pet.random()

        res_add = app.pet_api.add_pet(data=data, type_response=Pet)
        assert res_add.status_code == 200

        time.sleep(5)

        res_get = app.pet_api.get_by_id_pet(pet_id=res_add.data.id, type_response=Pet)

        time.sleep(5)

        assert res_get.status_code == 200, "Get request failed"
        assert isinstance(res_get.data, Pet), "Response data is not a Pet object"

        assert res_get.data.name == data.name, "Pet name mismatch"

    @pytest.mark.negative
    def test_get_pet_with_nonexistent_id(self, app):
        """
        Test retrieving a pet with a non-existent ID.
        Steps:
            1. Generate a non-existent pet ID.
            2. Attempt to retrieve a pet with this ID.
            3. Assert that the response status code is 404 (Not Found).
            4. Verify that the response contains "not found" message.
        Expected: API should return 404 Not Found.
        """
        non_existent_id = 999999999

        response = app.pet_api.get_by_id_pet(
            pet_id=non_existent_id, type_response=ApiResponse
        )

        assert (
            response.status_code == 404
        ), f"Expected: 404, Received: {response.status_code}"
        assert (
            "not found" in response.text.lower()
        ), "Response does not contain 'not found'"

    @pytest.mark.positive
    def test_update_pet(self, app):
        """
        Test for updating a pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Modify the pet's name and status.
            4. Update the pet through the API.
            5. Assert that the update was successful.
            6. Verify the updated fields match the expected values.
        """
        new_pet = Pet.random()

        created_pet = app.pet_api.add_pet(new_pet)
        assert created_pet.status_code == 200, "Failed to add pet"
        time.sleep(5)

        updated_pet = created_pet.json()
        updated_pet["name"] = "UpdatedPetName"
        updated_pet["status"] = "sold"

        response = app.pet_api.update_pet(Pet(**updated_pet))
        assert response.status_code == 200, "Failed to update pet"
        updated_data = response.json()

        assert updated_data["id"] == created_pet.json()["id"]
        assert updated_data["name"] == "UpdatedPetName"
        assert updated_data["status"] == "sold"

    @pytest.mark.positive
    def test_delete_pet(self, app):
        """
        Test for deleting a pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Delete the pet using its ID.
            4. Try to retrieve the pet by ID.
            5. Assert that the response status code for deletion is 200.
            6. Assert that retrieving the pet after deletion returns a 404.
        """
        data = Pet.random()

        res_add = app.pet_api.add_pet(data=data, type_response=Pet)

        assert res_add.status_code == 200

        time.sleep(3)

        res_delete = app.pet_api.delete_pet(pet_id=res_add.data.id)
        assert res_delete.status_code == 200, "Delete request failed"

        logging.info(f"Delete response: {res_delete.json()}")

        res_get = app.pet_api.get_by_id_pet(pet_id=data.id, type_response=Pet)

        if res_get.status_code == 200:
            logging.warning(f"Pet exists after deletion, response: {res_get.json()}")

        assert (
            res_get.status_code == 404
        ), f"Pet still exists after deletion. Status code: {res_get.status_code}"

    @pytest.mark.negative
    def test_delete_pet_with_nonexistent_id(self, app):
        """
        Test deleting a pet with a non-existent ID.
        Steps:
            1. Attempt to delete a pet with a non-existent ID.
            2. Assert that the response status code is 404 (Not Found).
            3. Verify the API correctly handles deletion of non-existent resources.
        Expected: API should return 404 Not Found.
        """
        response = app.pet_api.delete_pet(pet_id=999999999)
        assert (
            response.status_code == 404
        ), f"Expected: 404, Received: {response.status_code}"
