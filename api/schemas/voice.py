from pydantic import BaseModel
from datetime import datetime

class VoiceField(BaseModel):
  name: str
  embedding_path: str | None = None
  cliente_id: int

class VoiceResponse(BaseModel):
  id: int
  name: str
  embedding_path: str | None = None
  cliente_id: int
  created_at: datetime
 
  class Config:
    from_attributes: True

  def serializer_dt(self, dt: datetime, _info):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
