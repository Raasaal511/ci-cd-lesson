from abc import ABC, abstractmethod

from app.domain.entities import Catalog, Product


class CatalogRepository(ABC):
    @abstractmethod
    def add(self, catalog: Catalog) -> Catalog: ...

    @abstractmethod
    def get(self, catalog_id: int) -> Catalog | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Catalog | None: ...

    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 100) -> list[Catalog]: ...

    @abstractmethod
    def update(self, catalog: Catalog) -> Catalog: ...

    @abstractmethod
    def delete(self, catalog_id: int) -> None: ...


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product: ...

    @abstractmethod
    def get(self, product_id: int) -> Product | None: ...

    @abstractmethod
    def list_all(
        self, catalog_id: int | None = None, offset: int = 0, limit: int = 100
    ) -> list[Product]: ...

    @abstractmethod
    def update(self, product: Product) -> Product: ...

    @abstractmethod
    def delete(self, product_id: int) -> None: ...
