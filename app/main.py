from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine

from app.config import settings
from app.infrastructure.db.database import create_db_engine, create_session_factory, init_db
from app.presentation.api.errors import register_exception_handlers
from app.presentation.api.routers import catalogs, products


def create_app(engine: Engine | None = None) -> FastAPI:
    engine = engine or create_db_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        init_db(engine)
        yield
        engine.dispose()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.state.session_factory = create_session_factory(engine)

    register_exception_handlers(app)
    app.include_router(catalogs.router)
    app.include_router(products.router)

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
