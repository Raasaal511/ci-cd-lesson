import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.domain.entities import Catalog, Product
from app.infrastructure.db.models import ProductModel
from app.infrastructure.db.repositories import (
    SqlAlchemyCatalogRepository,
    SqlAlchemyProductRepository,
)


@pytest.fixture
def catalogs(session):
    return SqlAlchemyCatalogRepository(session)


@pytest.fixture
def products(session):
    return SqlAlchemyProductRepository(session)


def test_add_and_get_catalog(catalogs, session):
    created = catalogs.add(Catalog(name="Книги", description="Бумажные книги"))
    session.commit()

    assert created.id is not None
    assert catalogs.get(created.id) == created
    assert catalogs.get_by_name("Книги") == created


def test_get_missing_catalog_returns_none(catalogs):
    assert catalogs.get(999) is None
    assert catalogs.get_by_name("нет такого") is None


def test_list_catalogs_with_pagination(catalogs):
    for i in range(5):
        catalogs.add(Catalog(name=f"Каталог {i}"))

    page = catalogs.list_all(offset=1, limit=2)

    assert [c.name for c in page] == ["Каталог 1", "Каталог 2"]


def test_update_catalog(catalogs):
    created = catalogs.add(Catalog(name="Старое"))
    created.name = "Новое"

    updated = catalogs.update(created)

    assert updated.name == "Новое"
    assert catalogs.get(created.id).name == "Новое"


def test_catalog_name_is_unique_in_db(catalogs):
    catalogs.add(Catalog(name="Дубль"))
    with pytest.raises(IntegrityError):
        catalogs.add(Catalog(name="Дубль"))


def test_add_and_get_product(catalogs, products):
    catalog = catalogs.add(Catalog(name="Электроника"))

    created = products.add(Product(name="Ноутбук", price=999.9, quantity=3, catalog_id=catalog.id))

    assert created.id is not None
    assert products.get(created.id) == created


def test_list_products_filtered_by_catalog(catalogs, products):
    first = catalogs.add(Catalog(name="A"))
    second = catalogs.add(Catalog(name="B"))
    products.add(Product(name="a1", price=1, catalog_id=first.id))
    products.add(Product(name="b1", price=1, catalog_id=second.id))
    products.add(Product(name="a2", price=1, catalog_id=first.id))

    assert [p.name for p in products.list_all(catalog_id=first.id)] == ["a1", "a2"]
    assert len(products.list_all()) == 3


def test_update_and_delete_product(catalogs, products):
    catalog = catalogs.add(Catalog(name="Электроника"))
    product = products.add(Product(name="Телефон", price=100, catalog_id=catalog.id))

    product.price = 150
    assert products.update(product).price == 150

    products.delete(product.id)
    assert products.get(product.id) is None


def test_product_requires_existing_catalog(products):
    # PRAGMA foreign_keys=ON должен запрещать ссылку на несуществующий каталог.
    with pytest.raises(IntegrityError):
        products.add(Product(name="Сирота", price=1, catalog_id=12345))


def test_delete_catalog_cascades_to_products(catalogs, products, session):
    catalog = catalogs.add(Catalog(name="Удаляемый"))
    products.add(Product(name="p1", price=1, catalog_id=catalog.id))
    products.add(Product(name="p2", price=1, catalog_id=catalog.id))

    catalogs.delete(catalog.id)
    session.commit()

    assert session.scalar(select(func.count()).select_from(ProductModel)) == 0
