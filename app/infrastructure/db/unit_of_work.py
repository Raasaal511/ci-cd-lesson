from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from app.application.unit_of_work import UnitOfWork
from app.infrastructure.db.repositories import (
    SqlAlchemyCatalogRepository,
    SqlAlchemyProductRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> Self:
        self.session = self._session_factory()
        self.catalogs = SqlAlchemyCatalogRepository(self.session)
        self.products = SqlAlchemyProductRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
