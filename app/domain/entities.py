from dataclasses import dataclass

from app.domain.exceptions import DomainValidationError


@dataclass
class Catalog:
    name: str
    description: str | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise DomainValidationError("Название каталога не может быть пустым")


@dataclass
class Product:
    name: str
    price: float
    catalog_id: int
    description: str | None = None
    quantity: int = 0
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise DomainValidationError("Название товара не может быть пустым")
        if self.price < 0:
            raise DomainValidationError("Цена не может быть отрицательной")
        if self.quantity < 0:
            raise DomainValidationError("Количество не может быть отрицательным")

    @property
    def in_stock(self) -> bool:
        return self.quantity > 0
