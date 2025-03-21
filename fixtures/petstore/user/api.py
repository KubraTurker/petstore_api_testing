from requests import Response

from common.deco import logging as log
from fixtures.petstore.user.model import User
from fixtures.validator import Validator


class UserAPI(Validator):

    def __init__(self, app):
        """
        The UserAPI class contains helper methods for API operations related to users.
        :param app: The application object that provides the client to make API requests.
        """
        self.app = app

    POST_USER = "/user"  # Endpoint used to add a user
    GET_USER = "/user/{}"  # Endpoint used to get a user
    PUT_USER = "/user/{}"  # Endpoint used to update a user
    DELETE_USER = "/user/{}"  # Endpoint used to delete a user
    LOGIN_USER = "/user/login"  # User login endpoint
    LOGOUT_USER = "/user/logout"  # User logout endpoint

    @log("Adding new user")
    def add_user(self, data: User, type_response=User) -> Response:
        """
        Adds a new user.
        :param data: An object from the User model. This contains the data of the user to be added.
        :param type_response: (optional) Specifies the type to convert the response to (default is User).
        :return: The response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_USER}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    @log("Getting user by username")
    def get_user_by_username(self, username: str, type_response=User) -> Response:
        """
        Retrieves a user with the given username.
        :param username: The unique username of the user.
        :param type_response: (optional) Specifies the type to convert the response to (default is User).
        :return: The response containing the user's information.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_USER.format(username)}",
        )
        return self.structure(response, type_response=type_response)

    @log("Updating user")
    def update_user(self, data: User, type_response=User) -> Response:
        """
        Updates the information of a specific user.
        :param data: A User object containing the updated user information.
        :param type_response: (optional) Specifies the type to convert the response to.
        :return: The response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="PUT",
            url=f"{self.app.url}{self.PUT_USER.format(data.username)}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    @log("Deleting user")
    def delete_user(self, username: str) -> Response:
        """
        Deletes a specific user by their username.
        :param username: The username of the user to be deleted.
        :return: The response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_USER.format(username)}",
        )
        return response

    @log("User login")
    def login(self, username: str, password: str) -> Response:
        """
        Logs the user in with the given username and password.
        :param username: The user's username.
        :param password: The user's password.
        :return: The API response (Response object).
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.LOGIN_USER}",
            params={
                "username": username,
                "password": password,
            },
        )
        return response

    @log("User logout")
    def logout(self) -> Response:
        """
        Logs out the current user.
        :return: The API response (Response object).
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.LOGOUT_USER}",
        )
        return response
