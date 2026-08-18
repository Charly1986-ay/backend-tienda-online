import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import UserExistsException, UserNotFound
from .schemas import UserCreate, UserUpdate
from .models import User
from app.api.v1.users.repository import UserRepository
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)


    async def register(self, data: UserCreate) -> User:        
        existing_user = await self.user_repo.get_by_email(email=data.email)

        if existing_user:
            raise UserExistsException()
        
        user_db = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=get_password_hash(password=data.password),
            role=data.role,
            status=data.status
        )
        
        try:            
            await self.user_repo.create(user=user_db)
            await self.db.commit()
            await self.db.refresh(user_db)            
            
            logger.info(f"Nuevo usuario registrado exitosamente: {user_db.email} (ID: {user_db.id})")
            
            return user_db
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error al registrar el usuario {data.email}: {str(e)}")
            raise e


    async def update(self, data: UserUpdate, user_id: int) -> User:    
        user_db = await self.user_repo.get(user_id=user_id)

        if not user_db:
            raise UserNotFound()            
        
        updates = data.model_dump(exclude_unset=True)            
        
        if "password" in updates:
            plain_password = updates.pop("password")
            updates["hashed_password"] = get_password_hash(
                password=plain_password
            )

        try:            
            await self.user_repo.update(user=user_db, updates=updates)
            await self.db.commit()
            await self.db.refresh(user_db)            
                
            logger.info(f"Usuario actualizado exitosamente: {user_db.email} (ID: {user_db.id})")
                
            return user_db                
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error al actualizar el usuario {user_db.email}: {str(e)}")
            raise e