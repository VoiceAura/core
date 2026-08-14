from pydantic import BaseModel, Field, EmailStr, field_serializer
from datetime import datetime

class UserField(BaseModel):
  organization_id: int
  email: EmailStr
  password_hash: str
  first_name: str
  last_name: str
  role: str
  
  @field_serializer('email')
  def serialize_email(self, email: str, _info) -> str:
    return email.strip().lower()

  @field_serializer('first_name', 'last_name')
  def serialize_names(self, name: str, _info) -> str:
    return name.strip().title()

class UserResponse(BaseModel):
  id: int
  organization_id: int
  email: str
  first_name: str
  last_name: str
  created_at: datetime
 
  class Config:
    from_attributes: True

  def serializer_dt(self, dt: datetime, _info):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
