from dataclasses import replace
from typing import Any

from app.application.unit_of_work import UnitOfWork
from app.domain.entities import Catalog, Product
from app.domain.exceptions import (
    CatalogAlreadyExistsError,
    CatalogNotFoundError,
    ProductNotFoundError,
)


def _get_catalog_or_raise(uow: UnitOfWork, catalog_id: int) -> Catalog:
    catalog = uow.catalogs.get(catalog_id)
    if catalog is None:
        raise CatalogNotFoundError(catalog_id)
    return catalog


def _get_product_or_raise(uow: UnitOfWork, product_id: int) -> Product:
    product = uow.products.get(product_id)
    if product is None:
        raise ProductNotFoundError(product_id)
    return product


class CatalogService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def create(self, name: str, description: str | None = None) -> Catalog:
        catalog = Catalog(name=name, description=description)
        with self._uow as uow:
            if uow.catalogs.get_by_name(catalog.name) is not None:
                raise CatalogAlreadyExistsError(catalog.name)
            created = uow.catalogs.add(catalog)
            uow.commit()
        return created

    def get(self, catalog_id: int) -> Catalog:
        with self._uow as uow:
            return _get_catalog_or_raise(uow, catalog_id)

    def list_catalogs(self, offset: int = 0, limit: int = 100) -> list[Catalog]:
        with self._uow as uow:
            return uow.catalogs.list_all(offset=offset, limit=limit)

    def update(self, catalog_id: int, **changes: Any) -> Catalog:
        with self._uow as uow:
            catalog = _get_catalog_or_raise(uow, catalog_id)
            updated = replace(catalog, **changes)
            if updated.name != catalog.name and uow.catalogs.get_by_name(updated.name):
                raise CatalogAlreadyExistsError(updated.name)
            result = uow.catalogs.update(updated)
            uow.commit()
        return result

    def delete(self, catalog_id: int) -> None:
        with self._uow as uow:
            _get_catalog_or_raise(uow, catalog_id)
            uow.catalogs.delete(catalog_id)
            uow.commit()


class ProductService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def create(
        self,
        name: str,
        price: float,
        catalog_id: int,
        description: str | None = None,
        quantity: int = 0,
    ) -> Product:
        product = Product(
            name=name,
            price=price,
            catalog_id=catalog_id,
            description=description,
            quantity=quantity,
        )
        with self._uow as uow:
            _get_catalog_or_raise(uow, catalog_id)
            created = uow.products.add(product)
            uow.commit()
        return created

    def get(self, product_id: int) -> Product:
        with self._uow as uow:
            return _get_product_or_raise(uow, product_id)

    def list_products(
        self, catalog_id: int | None = None, offset: int = 0, limit: int = 100
    ) -> list[Product]:
        with self._uow as uow:
            if catalog_id is not None:
                _get_catalog_or_raise(uow, catalog_id)
            return uow.products.list_all(catalog_id=catalog_id, offset=offset, limit=limit)

    def update(self, product_id: int, **changes: Any) -> Product:
        with self._uow as uow:
            product = _get_product_or_raise(uow, product_id)
            updated = replace(product, **changes)
            if updated.catalog_id != product.catalog_id:
                _get_catalog_or_raise(uow, updated.catalog_id)
            result = uow.products.update(updated)
            uow.commit()
        return result

    def delete(self, product_id: int) -> None:
        with self._uow as uow:
            _get_product_or_raise(uow, product_id)
            uow.products.delete(product_id)
            uow.commit()
