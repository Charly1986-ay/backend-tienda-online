from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.movements import GenericActivityLog
from app.enums.movements import MovementType

class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get(self, id: str) -> GenericActivityLog | None:
        return await self.db.get(GenericActivityLog, id) 


    async def get_movements_by_user(self, user_id: int) -> list[GenericActivityLog]:
        result = await self.db.exec(
            select(GenericActivityLog).where(GenericActivityLog.user_id == user_id)
        )
        return list(result.all())


    async def get_movements_by_type(self, movement_type: MovementType) -> list[GenericActivityLog]:
        result = await self.db.exec(
            select(GenericActivityLog).where(GenericActivityLog.movement_type == movement_type)
        )
        return list(result.all())


    async def create_movement(self, log: GenericActivityLog) -> GenericActivityLog:           
        self.db.add(log)
        # Solo hacemos flush para que la base de datos le asigne un ID o prepare el objeto
        # sin cerrar la transacción todavía. El servicio hará el commit() final.
        await self.db.flush()
        await self.db.refresh(log)        
        return log