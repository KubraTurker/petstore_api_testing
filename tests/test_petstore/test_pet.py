import time
import logging
import pytest
import allure

from fixtures.petstore.pet.model import Pet, ApiResponse, Category


@allure.epic("Pet Store API")
@allure.feature("Pet Management")
class TestPet:

    @pytest.mark.positive
    @allure.story("Create Pets")
    @allure.title("Add a new pet to the store")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_pet(self, app):
        """
        Test for adding a new pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Assert that the status code is 200 (or 201).
            4. Assert that the response contains the pet ID and name.
        """
        with allure.step("Create a new pet object"):
            data = Pet.random()

        with allure.step("Add pet to the store"):
            res = app.pet_api.add_pet(data=data, type_response=Pet)
            allure.attach(
                str(data.__dict__), "Request Pet Data", allure.attachment_type.TEXT
            )
            allure.attach(
                str(res.data.__dict__), "Response Pet Data", allure.attachment_type.TEXT
            )

        with allure.step("Verify status code is 200"):
            assert res.status_code == 200

        with allure.step("Verify response data is a Pet object"):
            assert isinstance(res.data, Pet), "Response data is not a Pet object"

        with allure.step("Verify pet name matches"):
            assert res.data.name == data.name, "Pet name mismatch"

    @pytest.mark.negative
    @allure.story("Error Handling")
    @allure.title("Adding a pet with invalid status should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_pet_with_invalid_status(self, app):
        """
        Test for adding a pet with invalid status.
        Steps:
            1. Create a pet object with invalid status.
            2. Attempt to add the pet to the store.
            3. Assert that the status code is 400 or 500 (error).
            4. Verify the API rejects invalid status values.
        """
        with allure.step("Create a pet object with invalid status"):
            data = Pet(
                name="InvalidStatusPet",
                category=Category(id=1, name="Test Category"),
                photoUrls=["https://example.com/pet-photo.jpg"],
                tags=["test", "invalid"],
                status="invalid_status",
            )
            allure.attach(
                str(data.__dict__), "Invalid Pet Data", allure.attachment_type.TEXT
            )

        with allure.step("Attempt to add the pet to the store"):
            response = app.pet_api.add_pet(data=data, type_response=ApiResponse)
            allure.attach(response.text, "API Response", allure.attachment_type.TEXT)

        with allure.step("Verify error status code (400 or 500)"):
            assert response.status_code in [
                400,
                500,
            ], f"Expected: 400 or 500, Received: {response.status_code}"

    @pytest.mark.positive
    @allure.story("Retrieve Pets")
    @allure.title("Get pet by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_pet_by_id(self, app):
        """
        Test for retrieving a pet by ID.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Retrieve the pet by its ID using a retry mechanism.
            4. Assert that the response status code is 200.
            5. Assert that the retrieved pet has the same ID and name.
        """
        with allure.step("Create and add a new pet"):
            data = Pet.random()
            res_add = app.pet_api.add_pet(data=data, type_response=Pet)
            assert res_add.status_code == 200, "Failed to add pet"
            allure.attach(
                str(res_add.data.__dict__),
                "Created Pet Data",
                allure.attachment_type.TEXT,
            )

        @allure.step("Wait for pet to appear with ID {pet_id}")
        def wait_for_pet_to_appear(pet_id, retries=5, delay=1):
            for attempt in range(retries):
                allure.attach(
                    f"Attempt {attempt + 1}/{retries}",
                    "Retry Information",
                    allure.attachment_type.TEXT,
                )
                res_get = app.pet_api.get_by_id_pet(pet_id=pet_id, type_response=Pet)
                if res_get.status_code == 200:
                    return res_get
                time.sleep(delay)
            return res_get

        with allure.step(f"Retrieve pet with ID {res_add.data.id}"):
            res_get = wait_for_pet_to_appear(res_add.data.id)
            allure.attach(
                str(res_get.__dict__), "Get Pet Response", allure.attachment_type.TEXT
            )

        with allure.step("Verify response status code is 200"):
            assert res_get.status_code == 200, "Get request failed"

        with allure.step("Verify retrieved data is a Pet object"):
            assert isinstance(res_get.data, Pet), "Response data is not a Pet object"

        with allure.step("Verify pet ID matches"):
            assert res_get.data.id == res_add.data.id, "Pet ID mismatch"

        with allure.step("Verify pet name matches"):
            assert res_get.data.name == data.name, "Pet name mismatch"

    @pytest.mark.negative
    @allure.story("Error Handling")
    @allure.title("Get pet with non-existent ID should return 404")
    @allure.severity(allure.severity_level.NORMAL)
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
        with allure.step("Generate a non-existent pet ID"):
            non_existent_id = 999999999
            allure.attach(
                str(non_existent_id), "Non-existent ID", allure.attachment_type.TEXT
            )

        with allure.step("Attempt to retrieve pet with non-existent ID"):
            response = app.pet_api.get_by_id_pet(
                pet_id=non_existent_id, type_response=ApiResponse
            )
            allure.attach(response.text, "API Response", allure.attachment_type.TEXT)

        with allure.step("Verify response status code is 404"):
            assert (
                response.status_code == 404
            ), f"Expected: 404, Received: {response.status_code}"

        with allure.step("Verify response contains 'not found'"):
            assert (
                "not found" in response.text.lower()
            ), "Response does not contain 'not found'"

    @pytest.mark.positive
    @allure.story("Update Pets")
    @allure.title("Update an existing pet")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Create a new pet"):
            new_pet = Pet.random()
            allure.attach(
                str(new_pet.__dict__), "Original Pet Data", allure.attachment_type.TEXT
            )

        with allure.step("Add pet to the store"):
            created_pet = app.pet_api.add_pet(new_pet)
            assert created_pet.status_code == 200, "Failed to add pet"
            allure.attach(
                str(created_pet.json()),
                "Created Pet Response",
                allure.attachment_type.JSON,
            )
            time.sleep(5)

        with allure.step("Modify pet's name and status"):
            updated_pet = created_pet.json()
            updated_pet["name"] = "UpdatedPetName"
            updated_pet["status"] = "sold"
            allure.attach(
                str(updated_pet), "Modified Pet Data", allure.attachment_type.TEXT
            )

        with allure.step("Update the pet through API"):
            response = app.pet_api.update_pet(Pet(**updated_pet))
            assert response.status_code == 200, "Failed to update pet"
            updated_data = response.json()
            allure.attach(
                str(updated_data), "Update Response", allure.attachment_type.JSON
            )

        with allure.step("Verify updated fields"):
            assert updated_data["id"] == created_pet.json()["id"]
            assert updated_data["name"] == "UpdatedPetName"
            assert updated_data["status"] == "sold"

    @pytest.mark.positive
    @allure.story("Delete Pets")
    @allure.title("Delete a pet")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Create and add a new pet"):
            data = Pet.random()
            res_add = app.pet_api.add_pet(data=data, type_response=Pet)
            assert res_add.status_code == 200
            allure.attach(
                str(res_add.data.__dict__),
                "Created Pet Data",
                allure.attachment_type.TEXT,
            )

        with allure.step("Wait for the pet to be fully created"):
            time.sleep(3)

        with allure.step(f"Delete pet with ID {res_add.data.id}"):
            res_delete = app.pet_api.delete_pet(pet_id=res_add.data.id)
            assert res_delete.status_code == 200, "Delete request failed"
            logging.info(f"Delete response: {res_delete.json()}")
            allure.attach(
                str(res_delete.json()), "Delete Response", allure.attachment_type.JSON
            )

        with allure.step("Attempt to retrieve the deleted pet"):
            res_get = app.pet_api.get_by_id_pet(pet_id=data.id, type_response=Pet)
            allure.attach(
                str(res_get.status_code),
                "Get Deleted Pet Status Code",
                allure.attachment_type.TEXT,
            )
            time.sleep(10)

            if res_get.status_code == 200:
                logging.warning(
                    f"Pet exists after deletion, response: {res_get.json()}"
                )
                allure.attach(
                    str(res_get.json()), "Pet Still Exists", allure.attachment_type.JSON
                )

        with allure.step("Verify pet is no longer available"):
            assert (
                res_get.status_code == 404
            ), f"Pet still exists after deletion. Status code: {res_get.status_code}"

    @pytest.mark.negative
    @allure.story("Error Handling")
    @allure.title("Delete pet with non-existent ID should return 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_pet_with_nonexistent_id(self, app):
        """
        Test deleting a pet with a non-existent ID.
        Steps:
            1. Attempt to delete a pet with a non-existent ID.
            2. Assert that the response status code is 404 (Not Found).
            3. Verify the API correctly handles deletion of non-existent resources.
        Expected: API should return 404 Not Found.
        """
        with allure.step("Attempt to delete pet with non-existent ID"):
            non_existent_id = 999999999
            allure.attach(
                str(non_existent_id), "Non-existent ID", allure.attachment_type.TEXT
            )
            response = app.pet_api.delete_pet(pet_id=non_existent_id)
            allure.attach(
                str(response.status_code),
                "Delete Response Code",
                allure.attachment_type.TEXT,
            )

        with allure.step("Verify response status code is 404"):
            assert (
                response.status_code == 404
            ), f"Expected: 404, Received: {response.status_code}"
