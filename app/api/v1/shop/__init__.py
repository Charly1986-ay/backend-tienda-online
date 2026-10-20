from fastapi import APIRouter

from app.api.v1.shop.checkout.router import router as checkout_router
from app.api.v1.shop.articles.router import router as articles_router


router = APIRouter(prefix="/shop", tags=["Shop"])

# Los incluyes aquí dentro
router.include_router(checkout_router, prefix="/checkout", tags=["CheckOut - Shop"])
router.include_router(articles_router, prefix="/articles", tags=["Articles - Shop"])

