from pydantic import BaseModel, EmailStr

from app.api.v1.auth.schemas import UserCreate
from .enums import UserStatus


class UserUpdate(UserCreate):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None 


class UserUpdateStatus(BaseModel):
    status: UserStatus