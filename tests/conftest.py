from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.db.database import create_db_engine, create_session_factory, init_db
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.main import create_app


@pytest.fixture
def engine() -> Iterator[Engine]:
    """Новая in-memory SQLite БД на каждый тест."""
    engine = create_db_engine("sqlite://")
    init_db(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session_factory(engine: Engine) -> sessionmaker[Session]:
    return create_session_factory(engine)


@pytest.fixture
def session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    with session_factory() as session:
        yield session


@pytest.fixture
def uow(session_factory: sessionmaker[Session]) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


@pytest.fixture
def client(engine: Engine) -> Iterator[TestClient]:
    with TestClient(create_app(engine)) as client:
        yield client


@pytest.fixture
def catalog_id(client: TestClient) -> int:
    response = client.post("/catalogs", json={"name": "Электроника"})
    return response.json()["id"]
