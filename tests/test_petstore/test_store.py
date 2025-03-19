import time
import pytest
import logging

from fixtures.petstore.store.model import Order


class TestStore:

    @pytest.mark.positive
    def test_add_order(self, app):
        """
        Test for adding a new order.
        Steps:
            1. Create a new order object.
            2. Add the order to the store.
            3. Verify that the response status code is 200 (or 201).
            4. Validate the order ID in the response.
        """
        data = Order.random()
        res = app.store_api.add_order(data=data)

        assert res.status_code == 200
        assert isinstance(res.data, Order), "Response data is not an Order object"
        assert res.data.id == data.id, "Order ID does not match"

    @pytest.mark.positive
    def test_get_order_by_id(self, app):
        """
        Test for retrieving an order by its ID.
        Steps:
            1. Create a new order object.
            2. Add the order to the store.
            3. Retrieve the order by its ID.
            4. Verify that the response status code is 200.
            5. Validate the retrieved order's ID.
        """
        data = Order.random()
        res_add = app.store_api.add_order(data=data)
        assert res_add.status_code == 200

        time.sleep(5)

        res_get = app.store_api.get_order_by_id(
            order_id=res_add.data.id, type_response=Order
        )

        time.sleep(5)

        assert res_get.status_code == 200, "GET request failed"
        assert isinstance(res_get.data, Order), "Response data is not an Order object"
        assert res_get.data.id == data.id, "Order ID does not match"

    @pytest.mark.negative
    def test_get_nonexistent_order(self, app):
        """
        Test for retrieving a non-existent order.
        Steps:
            1. Try to get an order with a random or invalid ID.
            2. Verify that the response status code is 404.
        """
        invalid_order_id = 999999
        res_get = app.store_api.get_order_by_id(order_id=invalid_order_id)

        assert res_get.status_code == 404, "Expected 404 for non-existent order"

    @pytest.mark.positive
    def test_delete_order(self, app):
        """
        Test for deleting an order.
        Steps:
            1. Create a new order object.
            2. Add the order to the store.
            3. Delete the order.
            4. Try to retrieve the deleted order by ID.
            5. Verify that the deletion was successful.
            6. Confirm that the deleted order no longer exists (should return 404).
        """
        data = Order.random()
        res_add = app.store_api.add_order(data=data)
        assert res_add.status_code == 200  # or 201

        time.sleep(5)

        res_delete = app.store_api.delete_order(order_id=res_add.data.id)
        assert res_delete.status_code == 200, "Deletion failed"

        logging.info(f"Delete response: {res_delete.json()}")

        res_get = app.store_api.get_order_by_id(order_id=data.id)

        time.sleep(5)

        if res_get.status_code == 200:
            logging.warning(
                f"Order still exists after deletion, response: {res_get.json()}"
            )

        assert (
            res_get.status_code == 404
        ), f"Order still exists after deletion. Returned status code: {res_get.status_code}"
