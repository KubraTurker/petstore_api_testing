# Petstore API Test Automation
This project is an API Test Automation framework developed to test the Swagger Petstore API. It utilizes Python, Pytest, Requests to thoroughly test the API's endpoints.
## About the Project
The Petstore API is a system for managing users and pets in an e-commerce environment. This project includes tests for the following API operations:

### **1. User API Tests**

- Add a new user
- Retrieve user details
- Update an existing user
- Delete a user
- User login and logout 
- Retrieve and delete a non-existent user (negative tests)

### **2. Pet API Tests**
- Add a new pet
- Update pet details
- Retrieve pet information
- Delete a pet
- Retrieve a non-existent pet (negative test)

### **3.Store API Tests**

- Create an order
- Retrieve order details
- Delete an order
- Retrieve and delete a non-existent order (negative test)

**Goal:** To ensure that the Petstore API functions correctly and reliably through automated tests.

## Technologies Used

The following technologies and libraries are used in this project:

- Python 3.9+ → Used for writing tests
- Pytest → Used as the test framework
- Requests → Used for API requests

## Setup and Execution

**1.Install Dependencies**

```commandline
pip install -r requirements.txt
```
**2.Run Tests**

To execute the tests:
```commandline
pytest
```
## Test Scenarios

This project contains tests for various Swagger Petstore API endpoints. Below is an overview of the tested endpoints:

**1. User API Tests**

- Add User: Creates a new user and verifies the data.
- Get User Information: Retrieves a registered user’s details by username.
- Update User: Modifies user details and verifies the update.
- Delete User: Deletes a user from the system and ensures it cannot be retrieved.
- User Login and Logout: Validates successful login and logout operations.
- Negative Tests: Ensures that retrieving or deleting a non-existent user returns a 404 error.

**2. Pet API Tests**

- Add Pet: Adds a new pet and verifies its ID.
- Get Pet Information: Retrieves pet details by ID.
- Update Pet: Modifies pet details and confirms the update.
- Delete Pet: Ensures the pet is successfully removed from the system.
- Negative Tests: Ensures that retrieving a non-existent pet ID returns a 404 error.

**3. Store API Tests**

- Create Order: Places a new order and validates the response.
- Get Order Information: Retrieves order details using the order ID.
- Delete Order: Ensures the order is successfully deleted.
- Negative Tests: Ensures that retrieving a non-existent order ID returns a 404 error.