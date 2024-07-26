import datetime

from pydantic import EmailStr, UUID4,  Field, field_validator, BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data."""
    id: UUID4
    username: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
   
    @field_validator("password")
    def check_password(cls, value):
        """
        Validates the password's strength.

        Checks that the password meets the required criteria:
        - At least 8 characters long
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit

        Args:
            cls: The class to which the validator is applied.
            value: The password to validate.

        Raises:
            ValueError: If the password does not meet the criteria.
        
        Returns:
            str: The validated password.
        """
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
    """Schema for updating existing user details."""
    username: str = Field(None, min_length=1, max_length=30)
    email: EmailStr | None = Field(None)
