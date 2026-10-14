from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field
from app.utils.security_constants import validate_no_forbidden_words
from app.utils.slug import convert_slug


class NamedEntityBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)

    @field_validator('name', mode='after')
    @classmethod
    def check_name(cls, value: str) -> str:
        return validate_no_forbidden_words(value=value)

    @computed_field
    @property
    def slug(self) -> str:
        return convert_slug(title=self.name)


class NamedEntityResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        model_config = ConfigDict(from_attributes=True)