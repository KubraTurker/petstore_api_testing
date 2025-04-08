import time
import pytest
import logging
import allure

from fixtures.petstore.store.model import Order


@allure.epic("Pet Store API")
@allure.feature("Store Management")
class TestStore:

    @pytest.mark.positive
    @allure.story("Create Orders")
    @allure.title("Add a new order to the store")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_order(self, app):
        """
        Test for adding a new order.
        Steps:
            1. Create a new order object.
            2. Add the order to the store.
            3. Verify that the response status code is 200 (or 201).
            4. Validate the order ID in the response.
        """
        with allure.step("Create a new order object"):
            data = Order.random()
            allure.attach(
                str(data.__dict__), "Order Request Data", allure.attachment_type.TEXT
            )

        with allure.step("Add the order to the store"):
            res = app.store_api.add_order(data=data)
            allure.attach(
                str(res.status_code),
                "Response Status Code",
                allure.attachment_type.TEXT,
            )
            if hasattr(res, "text"):
                allure.attach(res.text, "Response Body", allure.attachment_type.TEXT)

        with allure.step("Verify response status code is 200"):
            assert res.status_code == 200

        with allure.step("Verify response data is an Order object"):
            assert isinstance(res.data, Order), "Response data is not an Order object"

        with allure.step("Verify order ID matches"):
            assert res.data.id == data.id, "Order ID does not match"

    @pytest.mark.positive
    @allure.story("Retrieve Orders")
    @allure.title("Get order by ID")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Create and add a new order"):
            data = Order.random()
            allure.attach(
                str(data.__dict__), "Order Request Data", allure.attachment_type.TEXT
            )
            res_add = app.store_api.add_order(data=data)
            assert res_add.status_code == 200
            allure.attach(
                str(res_add.data.__dict__),
                "Created Order Data",
                allure.attachment_type.TEXT,
            )

        with allure.step("Wait for order to be processed"):
            time.sleep(5)

        with allure.step(f"Retrieve order with ID {res_add.data.id}"):
            res_get = app.store_api.get_order_by_id(
                order_id=res_add.data.id, type_response=Order
            )
            allure.attach(
                str(res_get.status_code),
                "Get Response Status",
                allure.attachment_type.TEXT,
            )
            if hasattr(res_get, "text"):
                allure.attach(
                    res_get.text, "Get Response Body", allure.attachment_type.TEXT
                )

        with allure.step("Wait for response processing"):
            time.sleep(5)

        with allure.step("Verify get request status code is 200"):
            assert res_get.status_code == 200, "GET request failed"

        with allure.step("Verify response data is an Order object"):
            assert isinstance(
                res_get.data, Order
            ), "Response data is not an Order object"

        with allure.step("Verify order ID matches"):
            assert res_get.data.id == data.id, "Order ID does not match"

    @pytest.mark.negative
    @allure.story("Error Handling")
    @allure.title("Get non-existent order should return 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_order(self, app):
        """
        Test for retrieving a non-existent order.
        Steps:
            1. Try to get an order with a random or invalid ID.
            2. Verify that the response status code is 404.
        """
        with allure.step("Attempt to get order with invalid ID"):
            invalid_order_id = 999999
            allure.attach(
                str(invalid_order_id), "Invalid Order ID", allure.attachment_type.TEXT
            )
            res_get = app.store_api.get_order_by_id(order_id=invalid_order_id)
            allure.attach(
                str(res_get.status_code),
                "Response Status Code",
                allure.attachment_type.TEXT,
            )
            if hasattr(res_get, "text"):
                allure.attach(
                    res_get.text, "Response Body", allure.attachment_type.TEXT
                )

        with allure.step("Verify response status code is 404"):
            assert res_get.status_code == 404, "Expected 404 for non-existent order"

    @pytest.mark.positive
    @allure.story("Delete Orders")
    @allure.title("Delete an order")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Create and add a new order"):
            data = Order.random()
            allure.attach(
                str(data.__dict__), "Order Request Data", allure.attachment_type.TEXT
            )
            res_add = app.store_api.add_order(data=data)
            assert res_add.status_code == 200  # or 201
            allure.attach(
                str(res_add.data.__dict__),
                "Created Order Data",
                allure.attachment_type.TEXT,
            )

        with allure.step("Wait for order to be processed"):
            time.sleep(5)

        with allure.step(f"Delete order with ID {res_add.data.id}"):
            res_delete = app.store_api.delete_order(order_id=res_add.data.id)
            assert res_delete.status_code == 200, "Deletion failed"
            allure.attach(
                str(res_delete.json()), "Delete Response", allure.attachment_type.JSON
            )
            logging.info(f"Delete response: {res_delete.json()}")

        with allure.step("Attempt to retrieve the deleted order"):
            res_get = app.store_api.get_order_by_id(order_id=data.id)
            allure.attach(
                str(res_get.status_code),
                "Get Deleted Order Status",
                allure.attachment_type.TEXT,
            )
            time.sleep(10)
        with allure.step("Wait for response processing"):
            time.sleep(5)

        with allure.step("Verify order is no longer available"):
            if res_get.status_code == 200:
                logging.warning(
                    f"Order still exists after deletion, response: {res_get.json()}"
                )
                allure.attach(
                    str(res_get.json()),
                    "Order Still Exists",
                    allure.attachment_type.JSON,
                )

            assert (
                res_get.status_code == 404
            ), f"Order still exists after deletion. Returned status code: {res_get.status_code}"
