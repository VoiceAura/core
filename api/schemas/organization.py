from pydantic import BaseModel, field_serializer
from datetime import datetime

class OrganizationField(BaseModel):
  name: str
  slug: str
  status: bool
  
  @field_serializer('name')
  def serializer_name(name: str, _info) -> str:
    return name.strip().upper()

class OrganizationResponse(BaseModel):
  id: int
  name: str
  slug: str
  status: bool
  created_at: datetime
 
  class Config:
    from_attributes: True

  def serializer_dt(self, dt: datetime, _info):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
