from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import DateTime, String
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from db.Base import Base


if TYPE_CHECKING:
  from models.user import User

class Organization(Base):
  __tablename__ = "organizations"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  slug: Mapped[str] = mapped_column(String(20), unique=True)
  status: Mapped[bool] 
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )

  users: Mapped[List["User"]] = relationship(
                     back_populates="organization",
                     cascade="all, delete-orphan"
                     )

