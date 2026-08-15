from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base
from domain.voice_profile_models import VoiceProfileStatus

if TYPE_CHECKING:
  from models.organization import OrganizationModel
  from models.voice_sample import VoiceSampleModel

class VoiceProfileModel(Base):
  __tablename__ = "voice_profiles"

  id: Mapped[int] = mapped_column(primary_key=True)
  organization_id: Mapped[int] = mapped_column(
             ForeignKey("organizations.id")
             )
  name: Mapped[str]
  provider: Mapped[str]
  provider_voice_id: Mapped[str]

  status: Mapped[VoiceProfileStatus] = mapped_column(
        Enum(VoiceProfileStatus, name="voice_profile_status"),
        nullable=False,
        default=VoiceProfileStatus.PROCESSING,
    )
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )

  organization: Mapped["OrganizationModel"] = relationship(back_populates="voice_profiles")

  voice_samples: Mapped[list["VoiceSampleModel"]] = relationship(
                                                  back_populates="voice_profile",
                                                  cascade="all, delete-orphan")
