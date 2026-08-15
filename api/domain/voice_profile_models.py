from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class VoiceProfileStatus(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DISABLED = "disabled"

@dataclass(frozen=True)
class CreateVoiceProfile:
    organization_id: int
    name: str
    provider: str
    provider_voice_id: str
    status: VoiceProfileStatus

@dataclass(frozen=True)
class GetVoiceProfile:
    id: int

@dataclass(frozen=True)
class VoiceProfile:
    id: int
    organization_id: int
    name: str
    provider: str
    provider_voice_id: str
    status: VoiceProfileStatus
    created_at: datetime
