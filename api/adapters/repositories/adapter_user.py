from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import UserRepository
from domain.user_models import CreateUser, User
from models.organization import OrganizationModel
from models.user import UserModel


class AdapterUser(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_list(self) -> list[User]:
        query = select(UserModel)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return [
                User(
                    id=user.id,
                    organization_id=user.organization_id,
                    email=user.email,
                    password_hash=user.password_hash,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=user.role,
                    created_at=user.created_at
                )
                for user in users
            ]

    async def get_by_id(self, id: int) -> User | None:
        query = select(UserModel).where(UserModel.id == id)

        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return User(
            id=user.id,
            organization_id=user.organization_id,
            email=user.email,
            password_hash=user.password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            created_at=user.created_at
        )

    async def add(self, request: CreateUser) -> User:
            db_user = UserModel(
                organization_id=request.organization_id,
                email=request.email,
                password_hash=request.password_hash,
                first_name=request.first_name,
                last_name=request.last_name,
                role=request.role
            )

            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)

            return User(
                id=db_user.id,
                organization_id=db_user.organization_id,
                email=db_user.email,
                password_hash=db_user.password_hash,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                role=db_user.role,
                created_at=db_user.created_at
            )

    async def upgrade(self, id: int, request: CreateUser) -> User | None:
        user = await self.db.get(UserModel, id)
        if user is None:
            return None

        user.organization_id = request.organization_id
        user.email = request.email
        user.password_hash = request.password_hash
        user.first_name = request.first_name
        user.last_name = request.last_name
        user.role = request.role

        await self.db.commit()
        await self.db.refresh(user)

        return User(
            id=user.id,
            organization_id=user.organization_id,
            email=user.email,
            password_hash=user.password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            created_at=user.created_at
        )

    async def remove(self, id: int) -> None:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return

        await self.db.delete(user)
        return await self.db.commit()

    async def organization_existing(self, id: int) -> bool:
        org = await self.db.get(OrganizationModel, id)

        if not org:
            return False

        return True
