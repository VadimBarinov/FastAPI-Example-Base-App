from fastapi import APIRouter

from core.config import settings
from .users import router as users_router
from .dependencies_examples import router as dependencies_examples_router

router = APIRouter()

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)
router.include_router(
    dependencies_examples_router,
    prefix=settings.api.v1.dependencies,
)