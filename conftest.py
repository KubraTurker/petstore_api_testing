import pytest

from fixtures.app import Application


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        help="enter api url",
        default="https://petstore.swagger.io/v2",
    ),


@pytest.fixture(scope="session")
def app(request):
    url = request.config.getoption("--api-url")

    return Application(url)
