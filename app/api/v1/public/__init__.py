from fastapi import APIRouter

from app.api.v1.public.checkout.router import router as checkout_router


router = APIRouter(prefix="/public", tags=["Public"])

# Los incluyes aquí dentro
router.include_router(checkout_router, prefix="/checkout", tags=["CheckOut - Public"])
