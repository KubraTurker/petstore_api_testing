from requests import Response

from common.deco import logging as log
from fixtures.petstore.store.model import Order
from fixtures.validator import Validator


class StoreAPI(Validator):

    def __init__(self, app):
        """
        The StoreAPI class contains helper methods for store-related API operations.

        :param app: The application object that provides the client for making API requests.
        """
        self.app = app

    POST_ORDER = "/store/order"  # Endpoint used to add a new order
    GET_ORDER = "/store/order/{}"  # Endpoint used to retrieve an order
    DELETE_ORDER = "/store/order/{}"  # Endpoint used to delete an order

    @log("Adding a new order")
    def add_order(self, data: Order, type_response=Order) -> Response:
        """
        Adds a new order.

        :param data: An object from the Order model. This contains the data for the order to be added.
        :param type_response: (optional) Determines which type to convert the response to (Order by default).
        :return: The response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_ORDER}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    @log("Retrieving order by ID")
    def get_order_by_id(self, order_id: int, type_response=Order) -> Response:
        """
        Retrieves an order with the given ID.

        :param order_id: The unique identifier (ID) of the order.
        :param type_response: (optional) Determines which type to convert the response to (Order by default).
        :return: The response containing the order's information.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_ORDER.format(order_id)}",
        )
        return self.structure(response, type_response=type_response)

    @log("Deleting order by ID")
    def delete_order(self, order_id: int) -> Response:
        """
        Deletes a specific order by order ID.

        :param order_id: The unique identifier (ID) of the order to be deleted.
        :return: The response returned by the API (Response object).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_ORDER.format(order_id)}",
        )
        return response
