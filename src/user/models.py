from datetime import datetime
import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class User(SQLAlchemyBaseUserTable[uuid.UUID], Base):
    """SQLAlchemy model for the user table, representing user data in the database."""
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1023), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    verification_token: Mapped[str | None]

    def __doc__(self):
        return f"User({self.id}){self.username}"

    def __str__(self):
        return f"({self.id}) {self.username}"
