from pydantic import BaseModel, ConfigDict
from datetime import datetime
from domain.voice_profile_models import VoiceProfileStatus

class VoiceProfileField(BaseModel):
    organization_id: int
    name: str
    provider: str
    provider_voice_id: str
    status: VoiceProfileStatus

class VoiceProfileResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    provider: str
    provider_voice_id: str
    status: VoiceProfileStatus 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime, _info): # type: ignore
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')