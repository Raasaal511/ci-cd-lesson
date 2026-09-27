from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Catalog, Product
from app.domain.exceptions import CatalogNotFoundError, ProductNotFoundError
from app.domain.repositories import CatalogRepository, ProductRepository
from app.infrastructure.db.models import CatalogModel, ProductModel


def _to_catalog(model: CatalogModel) -> Catalog:
    return Catalog(id=model.id, name=model.name, description=model.description)


def _to_product(model: ProductModel) -> Product:
    return Product(
        id=model.id,
        name=model.name,
        description=model.description,
        price=model.price,
        quantity=model.quantity,
        catalog_id=model.catalog_id,
    )


class SqlAlchemyCatalogRepository(CatalogRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, catalog: Catalog) -> Catalog:
        model = CatalogModel(name=catalog.name, description=catalog.description)
        self.session.add(model)
        self.session.flush()
        return _to_catalog(model)

    def get(self, catalog_id: int) -> Catalog | None:
        model = self.session.get(CatalogModel, catalog_id)
        return _to_catalog(model) if model else None

    def get_by_name(self, name: str) -> Catalog | None:
        model = self.session.scalar(select(CatalogModel).where(CatalogModel.name == name))
        return _to_catalog(model) if model else None

    def list_all(self, offset: int = 0, limit: int = 100) -> list[Catalog]:
        stmt = select(CatalogModel).order_by(CatalogModel.id).offset(offset).limit(limit)
        return [_to_catalog(m) for m in self.session.scalars(stmt)]

    def update(self, catalog: Catalog) -> Catalog:
        model = self.session.get(CatalogModel, catalog.id)
        if model is None:
            raise CatalogNotFoundError(catalog.id)
        model.name = catalog.name
        model.description = catalog.description
        self.session.flush()
        return _to_catalog(model)

    def delete(self, catalog_id: int) -> None:
        model = self.session.get(CatalogModel, catalog_id)
        if model is not None:
            self.session.delete(model)
            self.session.flush()


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> Product:
        model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            catalog_id=product.catalog_id,
        )
        self.session.add(model)
        self.session.flush()
        return _to_product(model)

    def get(self, product_id: int) -> Product | None:
        model = self.session.get(ProductModel, product_id)
        return _to_product(model) if model else None

    def list_all(
        self, catalog_id: int | None = None, offset: int = 0, limit: int = 100
    ) -> list[Product]:
        stmt = select(ProductModel).order_by(ProductModel.id)
        if catalog_id is not None:
            stmt = stmt.where(ProductModel.catalog_id == catalog_id)
        stmt = stmt.offset(offset).limit(limit)
        return [_to_product(m) for m in self.session.scalars(stmt)]

    def update(self, product: Product) -> Product:
        model = self.session.get(ProductModel, product.id)
        if model is None:
            raise ProductNotFoundError(product.id)
        model.name = product.name
        model.description = product.description
        model.price = product.price
        model.quantity = product.quantity
        model.catalog_id = product.catalog_id
        self.session.flush()
        return _to_product(model)

    def delete(self, product_id: int) -> None:
        model = self.session.get(ProductModel, product_id)
        if model is not None:
            self.session.delete(model)
            self.session.flush()
