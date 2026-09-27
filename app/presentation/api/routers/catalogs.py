from fastapi import APIRouter, Query, status

from app.presentation.api.dependencies import CatalogServiceDep, ProductServiceDep
from app.presentation.api.schemas import CatalogCreate, CatalogRead, CatalogUpdate, ProductRead

router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_catalog(data: CatalogCreate, service: CatalogServiceDep) -> CatalogRead:
    return CatalogRead.model_validate(service.create(**data.model_dump()))


@router.get("")
def list_catalogs(
    service: CatalogServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[CatalogRead]:
    return [CatalogRead.model_validate(c) for c in service.list_catalogs(offset, limit)]


@router.get("/{catalog_id}")
def get_catalog(catalog_id: int, service: CatalogServiceDep) -> CatalogRead:
    return CatalogRead.model_validate(service.get(catalog_id))


@router.patch("/{catalog_id}")
def update_catalog(
    catalog_id: int, data: CatalogUpdate, service: CatalogServiceDep
) -> CatalogRead:
    catalog = service.update(catalog_id, **data.model_dump(exclude_unset=True))
    return CatalogRead.model_validate(catalog)


@router.delete("/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_catalog(catalog_id: int, service: CatalogServiceDep) -> None:
    service.delete(catalog_id)


@router.get("/{catalog_id}/products")
def list_catalog_products(
    catalog_id: int,
    service: ProductServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[ProductRead]:
    products = service.list_products(catalog_id=catalog_id, offset=offset, limit=limit)
    return [ProductRead.model_validate(p) for p in products]
