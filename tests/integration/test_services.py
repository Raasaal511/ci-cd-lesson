import pytest

from app.application.services import CatalogService, ProductService
from app.domain.entities import Catalog
from app.domain.exceptions import (
    CatalogAlreadyExistsError,
    CatalogNotFoundError,
    DomainValidationError,
    ProductNotFoundError,
)


@pytest.fixture
def catalog_service(uow):
    return CatalogService(uow)


@pytest.fixture
def product_service(uow):
    return ProductService(uow)


def test_created_catalog_is_persisted(catalog_service):
    created = catalog_service.create("Книги")

    # Новый UoW-контекст = новая сессия, значит данные реально закоммичены в БД.
    assert catalog_service.get(created.id) == created


def test_create_duplicate_catalog_fails(catalog_service):
    catalog_service.create("Книги")
    with pytest.raises(CatalogAlreadyExistsError):
        catalog_service.create("  Книги ")


def test_update_catalog_to_existing_name_fails(catalog_service):
    catalog_service.create("A")
    b = catalog_service.create("B")
    with pytest.raises(CatalogAlreadyExistsError):
        catalog_service.update(b.id, name="A")


def test_get_missing_catalog_fails(catalog_service):
    with pytest.raises(CatalogNotFoundError):
        catalog_service.get(42)


def test_create_product_in_missing_catalog_fails(product_service):
    with pytest.raises(CatalogNotFoundError):
        product_service.create(name="Товар", price=1, catalog_id=42)


def test_invalid_update_does_not_change_product(catalog_service, product_service):
    catalog = catalog_service.create("Электроника")
    product = product_service.create(name="Телефон", price=100, catalog_id=catalog.id)

    with pytest.raises(DomainValidationError):
        product_service.update(product.id, price=-10)

    assert product_service.get(product.id).price == 100


def test_move_product_to_another_catalog(catalog_service, product_service):
    a = catalog_service.create("A")
    b = catalog_service.create("B")
    product = product_service.create(name="Товар", price=1, catalog_id=a.id)

    product_service.update(product.id, catalog_id=b.id)

    assert product_service.list_products(catalog_id=a.id) == []
    assert [p.id for p in product_service.list_products(catalog_id=b.id)] == [product.id]


def test_move_product_to_missing_catalog_fails(catalog_service, product_service):
    catalog = catalog_service.create("A")
    product = product_service.create(name="Товар", price=1, catalog_id=catalog.id)

    with pytest.raises(CatalogNotFoundError):
        product_service.update(product.id, catalog_id=999)


def test_delete_catalog_removes_its_products(catalog_service, product_service):
    catalog = catalog_service.create("A")
    product = product_service.create(name="Товар", price=1, catalog_id=catalog.id)

    catalog_service.delete(catalog.id)

    with pytest.raises(ProductNotFoundError):
        product_service.get(product.id)


def test_rollback_when_commit_not_called(uow, catalog_service):
    with uow:
        uow.catalogs.add(Catalog(name="Черновик"))
        # commit() не вызван — изменения должны откатиться

    assert catalog_service.list_catalogs() == []
