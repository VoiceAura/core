from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base

if TYPE_CHECKING:
  from models.organization import OrganizationModel

class UserModel(Base):
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

  organization: Mapped["OrganizationModel"] = relationship(back_populates="users")
