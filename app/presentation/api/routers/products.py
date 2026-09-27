from fastapi import APIRouter, Query, status

from app.presentation.api.dependencies import ProductServiceDep
from app.presentation.api.schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, service: ProductServiceDep) -> ProductRead:
    return ProductRead.model_validate(service.create(**data.model_dump()))


@router.get("")
def list_products(
    service: ProductServiceDep,
    catalog_id: int | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[ProductRead]:
    products = service.list_products(catalog_id=catalog_id, offset=offset, limit=limit)
    return [ProductRead.model_validate(p) for p in products]


@router.get("/{product_id}")
def get_product(product_id: int, service: ProductServiceDep) -> ProductRead:
    return ProductRead.model_validate(service.get(product_id))


@router.patch("/{product_id}")
def update_product(
    product_id: int, data: ProductUpdate, service: ProductServiceDep
) -> ProductRead:
    product = service.update(product_id, **data.model_dump(exclude_unset=True))
    return ProductRead.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductServiceDep) -> None:
    service.delete(product_id)
