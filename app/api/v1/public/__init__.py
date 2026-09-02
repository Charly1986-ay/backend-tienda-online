from fastapi import APIRouter

from app.api.v1.public.checkout.router import router as checkout_router
from app.api.v1.public.articles.router import router as articles_router
from app.api.v1.public.users.router import router as users_router


router = APIRouter(prefix="/public", tags=["Public"])

# Los incluyes aquí dentro
router.include_router(checkout_router, prefix="/checkout", tags=["CheckOut - Public"])
router.include_router(articles_router, prefix="/articles", tags=["Articles - Public"])
router.include_router(users_router, prefix="/users", tags=["Users - Public"])
