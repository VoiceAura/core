from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from domain.organization_models import Organization, CreateOrganization
from domain.ports import OrganizationRepository
from models.organization import OrganizationModel


class AdapterOrganization(OrganizationRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_list(self) -> List[Organization]:
        query = select(OrganizationModel)
        result = await self.db.execute(query)
        organizations = result.scalars().all()
        return [
                Organization(
                    id=org.id,
                    name=org.name,
                    slug=org.slug,
                    status=org.status,
                    created_at=org.created_at,
                )
                for org in organizations
            ]

    async def get_by_id(self, id: int) -> Organization | None:
        query = select(OrganizationModel).where(OrganizationModel.id == id)

        result = await self.db.execute(query)
        org = result.scalar_one_or_none()

        if org is None:
            return None

        return Organization(
            id=org.id,
            name=org.name,
            slug=org.slug,
            status=org.status,
            created_at=org.created_at,
        )

    async def add(self, request: CreateOrganization) -> Organization:
            db_organization = OrganizationModel(
                name=request.name,
                slug=request.slug,
                status=request.status,
            )

            self.db.add(db_organization)
            await self.db.commit()
            await self.db.refresh(db_organization)

            return Organization(
                id=db_organization.id,
                name=db_organization.name,
                slug=db_organization.slug,
                status=db_organization.status,
                created_at=db_organization.created_at,
            )

    async def upgrade(self, id: int, request: CreateOrganization) -> Organization | None:
        query = select(OrganizationModel).where(OrganizationModel.id == id)
        result = await self.db.execute(query)
        org = result.scalar_one_or_none()

        if org is None:
            return None

        org.name = request.name
        org.slug = request.slug
        org.status = request.status

        await self.db.commit()
        await self.db.refresh(org)

        return Organization(
            id=org.id,
            name=org.name,
            slug=org.slug,
            status=org.status,
            created_at=org.created_at,
        )

    async def remove(self, id: int) -> None:
        query = select(OrganizationModel).where(OrganizationModel.id == id)

        result = await self.db.execute(query)
        org = result.scalar_one_or_none()

        if not result:
            return None

        await self.db.delete(org)
        await self.db.commit()
        return None
