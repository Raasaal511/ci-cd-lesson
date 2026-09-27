class DomainError(Exception):
    """Базовая ошибка предметной области."""


class DomainValidationError(DomainError):
    """Нарушены инварианты сущности."""


class NotFoundError(DomainError):
    """Сущность не найдена."""


class AlreadyExistsError(DomainError):
    """Сущность с такими данными уже существует."""


class CatalogNotFoundError(NotFoundError):
    def __init__(self, catalog_id: int) -> None:
        super().__init__(f"Каталог с id={catalog_id} не найден")
        self.catalog_id = catalog_id


class ProductNotFoundError(NotFoundError):
    def __init__(self, product_id: int) -> None:
        super().__init__(f"Товар с id={product_id} не найден")
        self.product_id = product_id


class CatalogAlreadyExistsError(AlreadyExistsError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Каталог с названием '{name}' уже существует")
        self.name = name
