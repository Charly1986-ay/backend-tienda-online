from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.utils.regex_validators import clean_string_spaces
from app.utils.regex_validators import validate_password_strength
from app.utils.security_constants import validate_no_forbidden_words
from .enums import Role, UserStatus


class UserValidate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None

    @field_validator('full_name')
    @classmethod
    def check_full_name(cls, value: str | None = None):
        if value is None:
            return value
        return validate_no_forbidden_words(value=value)
        
    @field_validator('password')
    @classmethod
    def check_password(cls, value: str | None = None):
        if value is None:
            return value
        return validate_password_strength(value)
        
    @field_validator('email', 'password', 'full_name', mode='before')
    @classmethod
    def clean_spaces(cls, value):
        return clean_string_spaces(value)


class UserCreate(UserValidate):
    email: EmailStr  # Sobrescribe los campos haciéndolo obligatorios
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


class UserUpdate(UserValidate):   
    pass


class UserUpdateStatus(BaseModel):
    status: UserStatus


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    status: UserStatus
    
    model_config = ConfigDict(from_attributes=True)