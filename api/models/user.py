from datetime import datetime
from typing import List
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from db.Base import Base


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  organization_id: Mapped[int] = mapped_column(
             ForeignKey("organizations.id")
             )
  email: Mapped[str] = mapped_column(String(100), unique=True)
  password_hash: Mapped[str]
  first_name: Mapped[str]
  last_name: Mapped[str]
  role: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )

  organization: Mapped["Organization"] = relationship(back_populates="users")
