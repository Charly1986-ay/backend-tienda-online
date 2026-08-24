from fastapi import APIRouter, Depends, HTTPException, status


from .schemas import TokenResponse, UserPublic, UserLogin
from app.services.auth import AuthService

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session
from app.core.exceptions import CredentialsException, UserNotFound
from app.utils.permission import get_current_user_active


router = APIRouter()

@router.post('/login', response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_session)
) -> TokenResponse:
    try:                
        auth_service = AuthService(db=db)
        token = await auth_service.authentication(login=login_data)
        
        return TokenResponse(
            access_token=token
        )
    except (UserNotFound, CredentialsException):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales no válidas'
        )


@router.get('/me', response_model=UserPublic)
async def get_profile(
    user = Depends(get_current_user_active)
) -> UserPublic:
    return user