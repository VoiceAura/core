from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base

if TYPE_CHECKING:
  from models.voice_profile import VoiceProfileModel

class VoiceSampleModel(Base):
  __tablename__ = "voice_samples"

  id: Mapped[int] = mapped_column(primary_key=True)
  voice_profile_id: Mapped[int] = mapped_column(
             ForeignKey("voice_profiles.id")
             )
  storage_reference: Mapped[str]
  duration: Mapped[float | None]
  format: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )

  voice_profile: Mapped["VoiceProfileModel"] = relationship(back_populates="voice_samples")
