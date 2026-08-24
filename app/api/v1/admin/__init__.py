from fastapi import APIRouter
from app.api.v1.admin.invoices.router import router as invoice_router
from app.api.v1.admin.articles.router import router as articles_router
from app.api.v1.admin.users.router import router as user_router
from app.api.v1.admin.categories.router import router as categories_router
from app.api.v1.admin.brands.router import router as brands_router


router = APIRouter(prefix="/admin", tags=["Admin"])

# Los incluyes aquí dentro
router.include_router(invoice_router, prefix="/invoices", tags=["Invoices - Admin"])
router.include_router(articles_router, prefix="/articles", tags=["Articles - Admin"])
router.include_router(user_router, prefix="/users", tags=["Users - Admin"])
router.include_router(categories_router, prefix="/categories", tags=["Categories - Admin"])
router.include_router(brands_router, prefix="/brands", tags=["Brands - Admin"])