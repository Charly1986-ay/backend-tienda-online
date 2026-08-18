from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.api.v1.users.enums import Role, UserStatus

if TYPE_CHECKING:    
    from app.api.v1.invoices.models import Invoice


class User(SQLModel, table=True):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    role: str = Field(default=Role.CLIENT.value, sa_column=Column(String))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    status: str = Field(default=UserStatus.ACTIVE.value, sa_column=Column(String))

    # Relación bidireccional con las facturas
    invoices: List['Invoice'] = Relationship(back_populates='client')