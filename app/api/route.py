from fastapi import APIRouter

from app.api.ai.api import router as ai_router
from app.api.auth.api import router as auth_router
from app.api.user.api import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(ai_router)
