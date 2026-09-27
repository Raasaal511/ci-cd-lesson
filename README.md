# Catalog Service

FastAPI-приложение с сущностями **Catalog** и **Product** (один каталог → много товаров),
построенное по принципам чистой архитектуры. БД — SQLite через SQLAlchemy 2.0.

## Структура

```
app/
├── domain/                 # Ядро: не зависит ни от FastAPI, ни от SQLAlchemy
│   ├── entities.py         # Catalog, Product (+ инварианты)
│   ├── exceptions.py       # доменные ошибки
│   └── repositories.py     # абстрактные интерфейсы репозиториев
├── application/            # Сценарии использования
│   ├── unit_of_work.py     # абстрактный Unit of Work (граница транзакции)
│   └── services.py         # CatalogService, ProductService
├── infrastructure/db/      # Реализация хранения
│   ├── models.py           # ORM-модели SQLAlchemy
│   ├── repositories.py     # SqlAlchemy*Repository
│   ├── unit_of_work.py     # SqlAlchemyUnitOfWork
│   └── database.py         # engine, sessionmaker, PRAGMA foreign_keys
├── presentation/api/       # HTTP-слой
│   ├── schemas.py          # Pydantic-схемы запросов/ответов
│   ├── dependencies.py     # DI: UoW → сервисы
│   ├── errors.py           # доменные ошибки → HTTP-коды
│   └── routers/            # /catalogs, /products
├── config.py
└── main.py                 # create_app()
```

Зависимости направлены только внутрь: `presentation → application → domain ← infrastructure`.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
```

Путь к БД задаётся переменной `DATABASE_URL` (по умолчанию `sqlite:///./app.db`).

## Тесты

```bash
pytest
```

Каждый тест получает свою чистую in-memory SQLite БД.

- `tests/unit` — инварианты доменных сущностей
- `tests/integration` — репозитории и сервисы на реальной SQLite (FK, каскадное удаление, уникальность, откат транзакций)
- `tests/api` — HTTP-эндпоинты через `TestClient`

## API

| Метод  | Путь                              | Описание                          |
|--------|-----------------------------------|-----------------------------------|
| POST   | `/catalogs`                       | создать каталог                   |
| GET    | `/catalogs?offset=&limit=`        | список каталогов                  |
| GET    | `/catalogs/{id}`                  | каталог по id                     |
| PATCH  | `/catalogs/{id}`                  | частичное обновление              |
| DELETE | `/catalogs/{id}`                  | удалить (вместе с товарами)       |
| GET    | `/catalogs/{id}/products`         | товары каталога                   |
| POST   | `/products`                       | создать товар                     |
| GET    | `/products?catalog_id=&offset=&limit=` | список товаров               |
| GET    | `/products/{id}`                  | товар по id                       |
| PATCH  | `/products/{id}`                  | частичное обновление              |
| DELETE | `/products/{id}`                  | удалить товар                     |
| GET    | `/health`                         | healthcheck                       |

Ошибки: `404` — не найдено, `409` — каталог с таким названием уже есть, `422` — невалидные данные.
