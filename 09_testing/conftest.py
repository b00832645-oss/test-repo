"""Fixtures shared by every test file in this folder (no import needed)."""
import pytest
from shop import OrderService, ProductRepository


@pytest.fixture
def repo():
    """A fresh repository for each test, so tests can't affect each other."""
    return ProductRepository()


@pytest.fixture
def order_service(repo):
    return OrderService(repo)
