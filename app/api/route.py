from fastapi import APIRouter

from app.api.ai.api import router as ai_router
from app.api.auth.api import router as auth_router
from app.api.dashboard.api import router as dashboard_router
from app.api.mock_test.api import router as mock_test_router
from app.api.practice.api import router as practice_router
from app.api.user.api import router as user_router
from app.api.vocabulary.api import router as vocabulary_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(ai_router)
router.include_router(dashboard_router)
router.include_router(mock_test_router)
router.include_router(user_router)
router.include_router(practice_router)
router.include_router(vocabulary_router)
