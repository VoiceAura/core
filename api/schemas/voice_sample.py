from pydantic import BaseModel, ConfigDict
from datetime import datetime

class VoiceSampleField(BaseModel):
    id: int
    voice_profile_id: int
    duration: float | None

class VoiceSampleResponse(BaseModel):
    id: int
    voice_profile_id: int
    storage_reference: str
    duration: float | None
    format: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime, _info): # type: ignore
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')