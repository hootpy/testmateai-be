from fastapi import APIRouter
from app.api.user.api import router as user_router
from app.api.auth.api import router as auth_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
