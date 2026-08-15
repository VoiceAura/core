from domain.errors import NOT_FOUND
from domain.organization_models import CreateOrganization, GetOrganization, Organization
from domain.ports import OrganizationRepository


async def get_organizations_use(
    org_repository: OrganizationRepository,
) -> list[Organization]:

    return await org_repository.get_list()

async def get_organization_case(request: GetOrganization, org_repository: OrganizationRepository) -> Organization:
    org = await org_repository.get_by_id(request.id)

    if org is None:
        raise NOT_FOUND(detail="Organization not found")

    return org

async def create_organization_case(request: CreateOrganization, org_repository: OrganizationRepository) -> Organization:
    return await org_repository.add(request)

async def update_organization_case(id: int, request: CreateOrganization, org_repository: OrganizationRepository) -> Organization | None:
    org = await org_repository.upgrade(id, request)

    if not org:
        raise NOT_FOUND(detail="Organization not found")

    return org

async def remove_organization_case(request: GetOrganization, org_repository: OrganizationRepository) -> None:
    org = await org_repository.get_by_id(request.id)

    if org is None:
        raise NOT_FOUND(detail="Organization not found")

    return await org_repository.remove(request.id)
