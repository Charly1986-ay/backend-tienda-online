from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Column, Field, SQLModel, String

from app.enums.movements import MovementType



class GenericActivityLog(SQLModel, table=True):
    __tablename__ = 'generic_activity_log'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Usuario que realiza la acción
    user_id: int = Field(foreign_key='user.id', index=True)
    
    # --- CAMPOS GENÉRICOS CON ENUMS ---
    target_type: str = Field(sa_column=Column(String, index=True))
    target_id: str = Field(index=True)           
    
    # Detalle de la operación
    movement_type: str = Field(
        default=MovementType.UPDATED.value, 
        sa_column=Column(String)
    )
    details: Optional[str] = Field(default=None)  # Ej: "Actualización de estado a activo"
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        nullable=False
    ) 