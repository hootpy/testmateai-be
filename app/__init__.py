from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.common.utils.version import get_project_version
from app.core.config import SETTINGS
from fastapi import FastAPI
from app.api.routes import router as api_router

from app.setup.database import sessionmanager
from app.setup.middleware import middlewares


def create_app() -> FastAPI:
    database_url = (
        f"postgresql+asyncpg://{SETTINGS.POSTGRES_USERNAME}:{SETTINGS.POSTGRES_PASSWORD}"
        f"@{SETTINGS.POSTGRES_SERVER}:{SETTINGS.POSTGRES_PORT}/{SETTINGS.POSTGRES_DATABASE}"
    )
    sessionmanager.init(database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    app = FastAPI(
        title="FastAPI Postgres API",
        version=get_project_version(),
        middleware=middlewares,
        description="Project template using FastAPI with PostgrsSQL",
        lifespan=lifespan,
        debug=SETTINGS.DEBUG,
    )

    app.include_router(api_router, prefix="/api")

    return app
