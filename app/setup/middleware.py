from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.core.config import SETTINGS

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=SETTINGS.ALLOW_ORIGINS,
        allow_credentials=SETTINGS.ALLOW_CREDENTIALS,
        allow_methods=SETTINGS.ALLOW_METHODS,
        allow_headers=SETTINGS.ALLOW_HEADERS,
    )
]
