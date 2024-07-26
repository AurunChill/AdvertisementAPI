import datetime

from pydantic import EmailStr, UUID4,  Field, field_validator, BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: UUID4
    username: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
   
    @field_validator("password")
    def check_password(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value


class UserUpdate(BaseModel):
    username: str = Field(None, min_length=1, max_length=30)
    email: EmailStr | None = Field(None)
