import time
import pytest

from fixtures.petstore.user.model import User


class TestUser:

    @pytest.mark.positive
    def test_add_user(self, app):
        """
        Test for adding a new user.
        Steps:
            1. Create a new random user object.
            2. Add the user to the system.
            3. Verify that the response status code is 200.
            4. Validate that the response data is a User object.
            5. Confirm that the username in the response matches the original data.
        """
        data = User.random()
        res = app.user_api.add_user(data=data)

        time.sleep(5)

        assert res.status_code == 200
        assert isinstance(res.data, User), "Response data is not a User object"
        assert res.data.username == data.username, "Username mismatch"

    @pytest.mark.positive
    def test_get_user_by_username(self, app):
        """
        Test for retrieving a user by username.
        Steps:
            1. Create a new random user object.
            2. Add the user to the system.
            3. Verify that the user was added successfully.
            4. Retrieve the user by username.
            5. Verify that the response status code is 200.
            6. Confirm that the retrieved username matches the original username.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data)
        assert res_add.status_code == 200

        time.sleep(5)

        res_get = app.user_api.get_user_by_username(username=data.username)
        assert res_get.status_code == 200, "Get request failed"
        assert res_get.data.username == data.username, "Username mismatch"

    @pytest.mark.negative
    def test_get_non_existent_user(self, app):
        """
        Test retrieving a non-existent user.
        Steps:
            1. Attempt to retrieve a user that does not exist in the system.
            2. Verify that the response status code is 404.
        """
        username = "nonexistentuser123"
        res = app.user_api.get_user_by_username(username=username)
        assert (
            res.status_code == 404
        ), "Expected status code 404, but received a different response."

    @pytest.mark.positive
    def test_update_user(self, app):
        """
        Test for updating user information.
        Steps:
           1. Create a new random user object.
           2. Add the user to the system.
           3. Verify that the user was added successfully.
           4. Update the user's first name and last name.
           5. Submit the update request.
           6. Verify that the update was successful.
           7. Retrieve the updated user information.
           8. Confirm that the first name and last name were updated correctly.
        """
        data = User.random()
        created_user = app.user_api.add_user(data)
        assert created_user.status_code == 200, "Kullanıcı oluşturulamadı"

        updated_user = created_user.data.to_dict()
        updated_user["firstName"] = "UpdatedFirstName"
        updated_user["lastName"] = "UpdatedLastName"

        response = app.user_api.update_user(User(**updated_user))
        assert response.status_code == 200, "Kullanıcı güncellenemedi"

        res_get = app.user_api.get_user_by_username(username=updated_user["username"])
        assert res_get.status_code == 200, "Güncellenmiş kullanıcı bilgileri alınamadı"

        get_user_data = res_get.data.to_dict()
        assert (
            get_user_data["firstName"] == "UpdatedFirstName"
        ), f"Beklenen UpdatedFirstName ancak {get_user_data['firstName']} alındı"
        assert (
            get_user_data["lastName"] == "UpdatedLastName"
        ), f"Beklenen UpdatedLastName ancak {get_user_data['lastName']} alındı"

    @pytest.mark.positive
    def test_delete_user(self, app):
        """
        Test for deleting a user.
        Steps:
            1. Create a new random user object.
            2. Add the user to the system.
            3. Verify that the user was added successfully.
            4. Delete the user by username.
            5. Verify that the deletion was successful with a 200 status code.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data, type_response=User)
        assert res_add.status_code == 200

        time.sleep(5)

        res_delete = app.user_api.delete_user(username=data.username)
        assert res_delete.status_code == 200, "Delete request failed"

    @pytest.mark.negative
    def test_delete_non_existent_user(self, app):
        """
        Test deleting a non-existent user.
        Steps:
            1. Attempt to delete a user that does not exist in the system.
            2. Verify that the response status code is 404.
        """
        username = "nonexistentuser123"
        res = app.user_api.delete_user(username=username)
        assert (
            res.status_code == 404
        ), "Deletion of a non-existent user was unexpectedly successful, error was expected."

    @pytest.mark.positive
    def test_user_login(self, app):
        """
        Test for user login.
        Steps:
            1. Create a new random user object.
            2. Add the user to the system.
            3. Verify that the user was added successfully.
            4. Attempt to login with the user's credentials.
            5. Verify that the login was successful with a 200 status code.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data, type_response=User)
        assert res_add.status_code == 200

        time.sleep(5)

        res_login = app.user_api.login(username=data.username, password=data.password)
        assert res_login.status_code == 200, "Login request failed"

    @pytest.mark.positive
    def test_user_logout(self, app):
        """
        Test for user logout.
        Steps:
            1. Send a logout request to the API.
            2. Verify that the logout was successful with a 200 status code.
        """
        res_logout = app.user_api.logout()
        assert res_logout.status_code == 200, "Logout request failed"
