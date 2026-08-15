from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateOrganization:
    name: str
    slug: str
    status: bool

@dataclass(frozen=True)
class GetOrganization:
    id: int

@dataclass(frozen=True)
class Organization:
    id: int
    name: str
    slug: str
    status: bool
    created_at: datetime
