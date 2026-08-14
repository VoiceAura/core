from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.organization import OrganizationField, OrganizationResponse
from db.Session import get_db
from models.organization import Organization

organization_router = APIRouter(tags=["organizations"])

@organization_router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(db: AsyncSession = Depends(get_db)) -> List[dict]:
  query = select(Organization)
  result = await db.execute(query)
  return result.scalars().all()

@organization_router.get("/{id}", response_model=OrganizationResponse)
async def get_organization(id: int, db: AsyncSession = Depends(get_db)) -> dict:
  query = select(Organization).where(Organization.id == id)
  result = await db.execute(query)
  organization = result.scalars().first()

  if not organization:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  return organization

@organization_router.post(
  "/",
  response_model=OrganizationResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_organization(organization: OrganizationField, db: AsyncSession = Depends(get_db)) -> dict:
  new_organization = Organization(**organization.model_dump())
  db.add(new_organization)
  await db.commit()
  await db.refresh(new_organization)
  return new_organization

@organization_router.put("/{id}", response_model=OrganizationResponse)
async def update_organization(
  id: int,
  organization: OrganizationField,
  db: AsyncSession = Depends(get_db)
  ) -> dict:

  query = select(Organization).where(Organization.id == id)
  result = await db.execute(query)
  db_organization = result.scalars().first()

  if not db_organization:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  data = organization.model_dump()
  for field, value in data.items():
    setattr(db_organization, field, value)
  await db.commit()
  await db.refresh(db_organization)
  return db_organization

@organization_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, db: AsyncSession = Depends(get_db)) -> None:
  query = select(Organization).where(Organization.id == id)
  result = await db.execute(query)
  organization = result.scalars().first()

  if not organization:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  await db.delete(organization)
  await db.commit()
  return None
