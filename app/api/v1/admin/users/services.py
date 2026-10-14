from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.movements.enums import MovementType
from app.api.v1.admin.movements.enums import TargetType

from app.models.users import User

from app.api.v1.users.repository import UserRepository

from app.api.v1.users.schemas import UserUpdate, UserUpdateStatus
from .schemas import AdminUserCreate

from app.core.security import get_password_hash
from app.core.exceptions import UserExistsException, UserNotFound

from app.api.v1.admin.movements.services import ActivityLogService
from app.utils.dates import getCurrentDateTime


class AdminUserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db=db)
        self.activity_log = ActivityLogService(db=db)

    
    async def register_account(
        self, 
        user: AdminUserCreate, 
        admin: User
    ) -> User:
        user_db = await self.user_repo.get_by_email(
            email=user.email
        )

        if user_db:
            raise UserExistsException()

        user_db = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=get_password_hash(
                password=user.password
            ),
            role=user.role
        )

        try:           
            user_response = await self.user_repo.create(user=user_db)

            await self.activity_log.create(
                user_id=admin.id,
                target_id=str(user_db.id),
                target_type=TargetType.USER,
                movement_type=MovementType.CREATED,
                details=(
                    f"Se ha registrado un usuario. {user_response.full_name} "
                    f"Rol: {user_response.role}, creado por {admin.full_name}, "
                    f"Fecha de creación: {getCurrentDateTime()}"
                ),
            )              
            
            await self.db.commit()
            await self.db.refresh(user_response)
            return user_response
        except Exception as e:           
            await self.db.rollback()
            raise e


    async def update_user(
        self, 
        user_id: int, 
        user: UserUpdate, 
        admin: User
    ) -> User:
        user_db = await self.user_repo.get(user_id=user_id)

        if not user_db:
            raise UserNotFound()

        # Validar si el email ya existe en OTRO usuario
        if user.email:
            email_validate = await self.user_repo.get_by_email(email=user.email)
            if email_validate and email_validate.id != user_id:
                raise UserExistsException()
        
        user_dict = user.model_dump(exclude_unset=True)
        
        if "password" in user_dict:
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

        try:
            user_response = await self.user_repo.update(
                user=user_db, 
                updates=user_dict
            )

            # Registrar el log de actualización
            await self.activity_log.create(
                user_id=admin.id,
                target_id=str(user_db.id),
                target_type=TargetType.USER,
                movement_type=MovementType.UPDATED,
                details=(
                    f"Se ha actualizado el usuario {user_response.full_name}. "
                    f"Modificado por el administrador {admin.full_name}. "
                    f"Fecha de modificación: {getCurrentDateTime()}"
                ),
            )

            await self.db.commit()
            await self.db.refresh(user_response)

            return user_response
        except Exception as e:
            await self.db.rollback()
            raise e


    async def deactivate_account(
        self, 
        user_id: int, 
        user: UserUpdateStatus, 
        admin: User
    ) -> User:
        user_db = await self.user_repo.get(user_id=user_id)

        if not user_db:
            raise UserNotFound()

        user_dict = user.model_dump(exclude_unset=True)        

        try:
            user_response = await self.user_repo.update(
                user=user_db, 
                updates=user_dict
            )

            await self.activity_log.create(
                user_id=admin.id,
                target_id=str(user_db.id),
                target_type=TargetType.USER,
                movement_type=MovementType.DEACTIVATED,
                details=(
                    f"Se ha eliminado el usuario {user_db.full_name}. "
                    f"Rol: {user_db.role} por {admin.full_name}. "
                    f"Fecha de baja: {getCurrentDateTime()}"
                ),
            )

            await self.db.commit()
            await self.db.refresh(user_response)
            return user_response
        except Exception as e:
            await self.db.rollback()
            raise e