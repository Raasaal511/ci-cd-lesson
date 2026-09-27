from pydantic import BaseModel, ConfigDict, Field, field_validator


def _reject_null(value):
    if value is None:
        raise ValueError("поле не может быть null")
    return value


class CatalogCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class CatalogUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None

    _name_not_null = field_validator("name")(_reject_null)


class CatalogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: float = Field(ge=0)
    quantity: int = Field(default=0, ge=0)
    catalog_id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)
    catalog_id: int | None = None

    _not_null = field_validator("name", "price", "quantity", "catalog_id")(_reject_null)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: float
    quantity: int
    in_stock: bool
    catalog_id: int
