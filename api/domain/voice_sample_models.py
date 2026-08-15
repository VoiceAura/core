from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateVoiceSample:
    voice_profile_id: int
    storage_reference: str
    duration: float | None
    format: str

@dataclass(frozen=True)
class GetVoiceSample:
    id: int

@dataclass(frozen=True)
class VoiceSample:
    id: int
    voice_profile_id: int
    storage_reference: str
    duration: float | None
    format: str
    created_at: datetime
