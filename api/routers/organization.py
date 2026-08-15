from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.adapter_organization import AdapterOrganization
from application.use_cases.organization import (create_organization_case,
                                                get_organization_case,
                                                get_organizations_use,
                                                remove_organization_case,
                                                update_organization_case)
from db.Session import get_db
from domain.organization_models import CreateOrganization, GetOrganization
from schemas.organization import OrganizationField, OrganizationResponse
from utils.response_util import to_response

router = APIRouter(
    prefix="/organizations",
    tags=["organization"]
    )

@router.get("/", response_model=list[OrganizationResponse])
async def get_organizations(db: AsyncSession = Depends(get_db)) -> list[OrganizationResponse]:
    adapter = AdapterOrganization(db)
    result = await get_organizations_use(adapter)
    return [
		to_response(OrganizationResponse, organization)
		for organization in result
	]

@router.get("/{id}", response_model=OrganizationResponse)
async def get_organization(id: int, db: AsyncSession = Depends(get_db)) -> OrganizationResponse:
    adapter = AdapterOrganization(db)
    request = GetOrganization(id=id)
    result = await get_organization_case(request, adapter)

    return to_response(OrganizationResponse, result)

@router.post(
  "/",
  response_model=OrganizationResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_organization(organization: OrganizationField, db: AsyncSession = Depends(get_db)) -> OrganizationResponse:
    adapter = AdapterOrganization(db)
    request = CreateOrganization(name=organization.name,
                                slug=organization.slug,
                                status=organization.status)
    result = await create_organization_case(request, adapter)
    return to_response(OrganizationResponse, result)

@router.put("/{id}", response_model=OrganizationResponse)
async def update_organization(
        id: int,
        organization: OrganizationField,
        db: AsyncSession = Depends(get_db)
        ) -> OrganizationResponse:
    adapter = AdapterOrganization(db)
    request = CreateOrganization(name=organization.name,
                            slug=organization.slug,
                            status=organization.status)
    result = await update_organization_case(id, request, adapter)
    return to_response(OrganizationResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, db: AsyncSession = Depends(get_db)) -> None:
    adapter = AdapterOrganization(db)
    request = GetOrganization(id=id)
    
    return  await remove_organization_case(request, adapter)
