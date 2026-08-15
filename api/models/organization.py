from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base

if TYPE_CHECKING:
  from models.user import UserModel
  from models.voice_profile import VoiceProfileModel

class OrganizationModel(Base):
  __tablename__ = "organizations"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  slug: Mapped[str] = mapped_column(String(20), unique=True)
  status: Mapped[bool] 
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )

  users: Mapped[List["UserModel"]] = relationship(
                              back_populates="organization",
                              cascade="all, delete-orphan")

  voice_profiles: Mapped[List["VoiceProfileModel"]] = relationship(
                                                back_populates="organization",
                                                cascade="all, delete-orphan")
