from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime

class OrganizationField(BaseModel):
  name: str
  slug: str
  status: bool
  
  @field_serializer('name')
  def serializer_name(name: str, _info) -> str: # type: ignore
    return name.strip().upper()

class OrganizationResponse(BaseModel):
  id: int
  name: str
  slug: str
  status: bool
  created_at: datetime
 
  model_config = ConfigDict(from_attributes=True)

  def serializer_dt(self, dt: datetime, _info): # type: ignore
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
