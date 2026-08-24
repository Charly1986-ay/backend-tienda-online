import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.invoice import Role, UserStatus
from app.utils.security_constants import validate_no_forbidden_words
from app.utils.regex_validators import validate_password_strength

class UserValidatedBase(BaseModel):
    @field_validator('full_name')
    @classmethod
    def check_full_name(cls, value: Optional[str]):
        if value is None:
            return value
        return validate_no_forbidden_words(value=value)

    @field_validator('password')
    @classmethod
    def check_password(cls, value: Optional[str]):
        # Si es None (como en el Update cuando no lo mandan), lo dejamos pasar
        if value is None:
            return value
        return validate_password_strength(value)

    @field_validator('email', 'password', 'full_name', mode='before')
    @classmethod
    def clean_spaces(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(
        ..., 
        min_length=5, 
        max_length=50,
        description='The full name of the user, including first and last names.'
    )
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=15,
        description='Password must contain at least one uppercase letter and one special character.'
    )
    role: Role = Role.CLIENT.value
    status: UserStatus = UserStatus.ACTIVE.value


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None    


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    status: UserStatus
    model_config = ConfigDict(from_attributes=True)