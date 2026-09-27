from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.domain.repositories import CatalogRepository, ProductRepository


class UnitOfWork(ABC):
    """Граница транзакции: всё, что сделано внутри `with`, фиксируется только через commit()."""

    catalogs: CatalogRepository
    products: ProductRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        # После commit() откат ничего не делает, без commit() — отменяет изменения.
        self.rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
