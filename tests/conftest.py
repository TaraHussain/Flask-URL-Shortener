
from ..server import server as flask_app
import pytest


@pytest.fixture
def server():
    yield flask_app


@pytest.fixture
def client(server):
    server.testing = True
    return server.test_client()
