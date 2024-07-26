from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Advertisement(Base):
    __tablename__ = "advertisement"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(length=100))
    author: Mapped[str] = mapped_column(String)
    views_count: Mapped[int] = mapped_column(Integer, default=0)  
    position: Mapped[int] = mapped_column(Integer, nullable=True)

    def __doc__(self):
        return f"Advertisement({self.id}) {self.title} | Author ID: {self.author_id}"

    def __str__(self):
        return f"({self.id}) {self.title} | Author ID: {self.author_id}"