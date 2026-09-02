from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import get_session
from app.core.security import oauth2_schema, decode_token
from app.core.exceptions import CredentialsException, UserInactiveException, ForbiddenException
from app.models.users import User, UserStatus, Role
from app.repositories.users import UserRepository

async def get_current_user(
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_session)
) -> User:
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException()
    except Exception:
        raise CredentialsException()

    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(email=email)
    
    if not user:
        raise CredentialsException()
        
    return user


async def get_current_user_active(user: User = Depends(get_current_user)) -> User:
    if user.status == UserStatus.INACTIVE.value:
        raise UserInactiveException()
    return user


def require_roles(*allowed_roles: Role):
    async def role_checker(user: User = Depends(get_current_user_active)) -> User:
        # Validamos contra los valores string del enum almacenados en la BD
        if user.role not in [r.value for r in allowed_roles]:
            raise ForbiddenException()
        return user
    return role_checker


# --- Atajos de Dependencias para tus Rutas ---
manager_dependency = Depends(require_roles(Role.MANAGER))
manager_assistant_dependency = Depends(require_roles(Role.ECOMMERCE_ASSISTANT, Role.MANAGER))
ecommerce_assistant_dependency = Depends(require_roles(Role.ECOMMERCE_ASSISTANT))
client_dependency = Depends(require_roles(Role.CLIENT))
it_support_specialist = Depends(require_roles(Role.IT_SUPPORT_ESPECIALIST))