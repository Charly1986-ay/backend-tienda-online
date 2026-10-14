from fastapi import APIRouter

from app.api.v1.store.checkout.router import router as checkout_router
from app.api.v1.store.articles.router import router as articles_router


router = APIRouter(prefix="/store", tags=["Store"])

# Los incluyes aquí dentro
router.include_router(checkout_router, prefix="/checkout", tags=["CheckOut - Store"])
router.include_router(articles_router, prefix="/articles", tags=["Articles - Store"])

