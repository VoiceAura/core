from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateUser:
    organization_id: int
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: str

@dataclass(frozen=True)
class GetUser:
    id: int

@dataclass(frozen=True)
class User:
    id: int
    organization_id: int
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime
