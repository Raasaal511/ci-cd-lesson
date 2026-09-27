import pytest

from app.domain.entities import Catalog, Product
from app.domain.exceptions import DomainValidationError


def test_catalog_name_is_stripped():
    assert Catalog(name="  Книги  ").name == "Книги"


def test_catalog_empty_name_is_rejected():
    with pytest.raises(DomainValidationError):
        Catalog(name="   ")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"name": "", "price": 10},
        {"name": "Товар", "price": -1},
        {"name": "Товар", "price": 10, "quantity": -5},
    ],
)
def test_product_invalid_data_is_rejected(kwargs):
    with pytest.raises(DomainValidationError):
        Product(catalog_id=1, **kwargs)


@pytest.mark.parametrize(("quantity", "expected"), [(0, False), (3, True)])
def test_product_in_stock(quantity, expected):
    assert Product(name="Товар", price=1, catalog_id=1, quantity=quantity).in_stock is expected
