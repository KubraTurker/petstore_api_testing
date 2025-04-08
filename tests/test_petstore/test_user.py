import time
import pytest
import allure

from fixtures.petstore.user.model import User


@allure.epic("User Endpoint Tests")
class TestUser:

    @pytest.mark.positive
    @allure.story("Create User")
    @allure.title("Add a new user to the system")
    def test_add_user(self, app):
        with allure.step("Create a new random user object"):
            data = User.random()
            allure.attach(
                str(data.__dict__), "User Request Data", allure.attachment_type.TEXT
            )

        with allure.step("Add the user to the system"):
            res = app.user_api.add_user(data=data)
            allure.attach(
                str(res.status_code),
                "Response Status Code",
                allure.attachment_type.TEXT,
            )
            if hasattr(res, "text"):
                allure.attach(res.text, "Response Body", allure.attachment_type.TEXT)

        time.sleep(5)

        with allure.step("Verify status code is 200"):
            assert res.status_code == 200

        with allure.step("Verify response is a User object"):
            assert isinstance(res.data, User)

        with allure.step("Verify username matches"):
            assert res.data.username == data.username

    @pytest.mark.positive
    @allure.story("Get User")
    @allure.title("Retrieve a user by username")
    def test_get_user_by_username(self, app):
        with allure.step("Create and add a new user"):
            data = User.random()
            res_add = app.user_api.add_user(data=data)
            assert res_add.status_code == 200

        time.sleep(10)

        with allure.step("Get user by username"):
            res_get = app.user_api.get_user_by_username(username=data.username)
            allure.attach(
                str(res_get.status_code),
                "Response Status Code",
                allure.attachment_type.TEXT,
            )

            time.sleep(5)

            assert res_get.status_code == 200
            assert res_get.data.username == data.username

    @pytest.mark.negative
    @allure.story("Get User")
    @allure.title("Attempt to retrieve a non-existent user")
    def test_get_non_existent_user(self, app):
        with allure.step("Try to get a non-existent user"):
            username = "nonexistentuser123"
            res = app.user_api.get_user_by_username(username=username)
            assert res.status_code == 404

    @pytest.mark.positive
    @allure.story("Update User")
    @allure.title("Update an existing user's information")
    def test_update_user(self, app):
        with allure.step("Create and add a user"):
            data = User.random()
            created_user = app.user_api.add_user(data)
            assert created_user.status_code == 200

        with allure.step("Update user's first and last name"):
            updated_user = created_user.data.to_dict()
            updated_user["firstName"] = "UpdatedFirstName"
            updated_user["lastName"] = "UpdatedLastName"

        with allure.step("Submit update request"):
            response = app.user_api.update_user(User(**updated_user))
            assert response.status_code == 200
            time.sleep(5)

        with allure.step("Get updated user and verify changes"):
            res_get = app.user_api.get_user_by_username(
                username=updated_user["username"]
            )
            time.sleep(10)
            assert res_get.status_code == 200
            get_user_data = res_get.data.to_dict()
            assert get_user_data["firstName"] == "UpdatedFirstName"
            assert get_user_data["lastName"] == "UpdatedLastName"

    @pytest.mark.positive
    @allure.story("Delete User")
    @allure.title("Delete an existing user")
    def test_delete_user(self, app):
        with allure.step("Create and add a user"):
            data = User.random()
            res_add = app.user_api.add_user(data=data, type_response=User)
            assert res_add.status_code == 200

        time.sleep(5)

        with allure.step("Delete the user by username"):
            res_delete = app.user_api.delete_user(username=data.username)
            assert res_delete.status_code == 200

    @pytest.mark.negative
    @allure.story("Delete User")
    @allure.title("Attempt to delete a non-existent user")
    def test_delete_non_existent_user(self, app):
        with allure.step("Try deleting a non-existent user"):
            username = "nonexistentuser123"
            res = app.user_api.delete_user(username=username)
            assert res.status_code == 404

    @pytest.mark.positive
    @allure.story("User Authentication")
    @allure.title("Login with valid user credentials")
    def test_user_login(self, app):
        with allure.step("Create and add a user"):
            data = User.random()
            res_add = app.user_api.add_user(data=data, type_response=User)
            assert res_add.status_code == 200

        time.sleep(5)

        with allure.step("Login with user's credentials"):
            res_login = app.user_api.login(
                username=data.username, password=data.password
            )
            assert res_login.status_code == 200

    @pytest.mark.positive
    @allure.story("User Authentication")
    @allure.title("Logout user from the system")
    def test_user_logout(self, app):
        with allure.step("Logout from the system"):
            res_logout = app.user_api.logout()
            assert res_logout.status_code == 200
