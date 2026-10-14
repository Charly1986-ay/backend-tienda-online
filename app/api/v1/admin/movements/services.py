from sqlmodel.ext.asyncio.session import AsyncSession

from .enums import MovementType, TargetType
from app.models.movements import GenericActivityLog
from .repositoy import ActivityRepository


class ActivityLogService:
    def __init__(self, db: AsyncSession):
        self.activity_repo = ActivityRepository(db=db)

    async def create(
        self,
        user_id: int,
        target_id: str,
        target_type: TargetType,
        movement_type: MovementType,
        details: str,
    ) -> None:
        log = GenericActivityLog(
            user_id=user_id,
            target_type=target_type.value,
            target_id=target_id,
            movement_type=movement_type.value,
            details=details,
        )

        await self.activity_repo.create_movement(log=log)