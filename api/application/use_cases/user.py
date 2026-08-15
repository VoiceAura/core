from domain.errors import CONFLICT, NOT_FOUND
from domain.user_models import CreateUser, GetUser, User
from domain.ports import UserRepository


async def get_users_case(
    user_repository: UserRepository,
) -> list[User]:

    return await user_repository.get_list()

async def get_user_case(request: GetUser, user_repository: UserRepository) -> User:
    user = await user_repository.get_by_id(request.id)

    if user is None:
        raise NOT_FOUND(detail="User not found")

    return user

async def create_user_case(request: CreateUser, user_repository: UserRepository) -> User:
    org = await user_repository.organization_existing(request.organization_id)

    if org:
        raise CONFLICT(detail="Organization already exists")

    return await user_repository.add(request)

async def update_user_case(id: int, request: CreateUser, user_repository: UserRepository) -> User | None:

    org = await user_repository.organization_existing(request.organization_id)

    if not org:
        raise NOT_FOUND(detail=f"Organization ID: {request.organization_id} not found")
    
    user = await user_repository.upgrade(id, request)

    if not user:
        raise NOT_FOUND(detail="User not found")

    return user

async def remove_user_case(request: GetUser, user_repository: UserRepository) -> None:
    user = await user_repository.get_by_id(request.id)

    if user is None:
        raise NOT_FOUND(detail="User not found")

    return await user_repository.remove(request.id)
