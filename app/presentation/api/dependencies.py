from typing import Annotated

from fastapi import Depends, Request

from app.application.services import CatalogService, ProductService
from app.application.unit_of_work import UnitOfWork
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


def get_uow(request: Request) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(request.app.state.session_factory)


def get_catalog_service(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> CatalogService:
    return CatalogService(uow)


def get_product_service(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> ProductService:
    return ProductService(uow)


CatalogServiceDep = Annotated[CatalogService, Depends(get_catalog_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
