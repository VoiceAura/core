from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import VoiceProfileRepository
from domain.voice_profile_models import CreateVoiceProfile, VoiceProfile
from models.voice_profile import VoiceProfileModel
from models.organization import OrganizationModel


class AdapterVoiceProfile(VoiceProfileRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_list(self) -> list[VoiceProfile]:
        query = select(VoiceProfileModel)
        result = await self.db.execute(query)
        voice_profiles = result.scalars().all()

        return [
                VoiceProfile(
                    id=voice_profile.id,
                    organization_id=voice_profile.organization_id,
                    name=voice_profile.name,
                    provider=voice_profile.provider,
                    provider_voice_id=voice_profile.provider_voice_id,
                    status=voice_profile.status,
                    created_at=voice_profile.created_at
                )
                for voice_profile in voice_profiles
            ]

    async def get_by_organization_id(self, organization_id: int) -> list[VoiceProfile]:
        query = select(VoiceProfileModel).where(
                            VoiceProfileModel.organization_id == organization_id
                        )
        result = await self.db.execute(query)
        voice_profiles = result.scalars().all()

        return [
                VoiceProfile(
                    id=voice_profile.id,
                    organization_id=voice_profile.organization_id,
                    name=voice_profile.name,
                    provider=voice_profile.provider,
                    provider_voice_id=voice_profile.provider_voice_id,
                    status=voice_profile.status,
                    created_at=voice_profile.created_at
                )
                for voice_profile in voice_profiles
            ]

    async def add(self, request: CreateVoiceProfile) -> VoiceProfile:
            db_voice_profile = VoiceProfileModel(
                organization_id=request.organization_id,
                name=request.name,
                provider=request.provider,
                provider_voice_id=request.provider_voice_id,
                status=request.status
            )

            self.db.add(db_voice_profile)
            await self.db.commit()
            await self.db.refresh(db_voice_profile)

            return VoiceProfile(
                id=db_voice_profile.id,
                organization_id=db_voice_profile.organization_id,
                name=db_voice_profile.name,
                provider=db_voice_profile.provider,
                provider_voice_id=db_voice_profile.provider_voice_id,
                status=db_voice_profile.status,
                created_at=db_voice_profile.created_at
            )

    async def upgrade(self, id: int, request: CreateVoiceProfile) -> VoiceProfile | None:
        db_voice_profile = await self.db.get(VoiceProfileModel, id)
        if not db_voice_profile:
            return None

        db_voice_profile.organization_id = request.organization_id
        db_voice_profile.name = request.name
        db_voice_profile.provider = request.provider
        db_voice_profile.provider_voice_id = request.provider_voice_id
        db_voice_profile.status = request.status

        await self.db.commit()
        await self.db.refresh(db_voice_profile)

        return VoiceProfile(
             id=db_voice_profile.id,
            organization_id=db_voice_profile.organization_id,
            name=db_voice_profile.name,
            provider=db_voice_profile.provider,
            provider_voice_id=db_voice_profile.provider_voice_id,
            status=db_voice_profile.status,
            created_at=db_voice_profile.created_at
        )

    async def remove(self, id: int) -> None:
        query = select(VoiceProfileModel).where(VoiceProfileModel.id == id)
        result = await self.db.execute(query)
        voice_profile = result.scalar_one_or_none()

        if not voice_profile:
            return

        await self.db.delete(voice_profile)
        return await self.db.commit()

    async def organization_existing(self, id: int) -> bool:
        org = await self.db.get(OrganizationModel, id)

        if not org:
            return False

        return True

    async def voice_profile_existing(self, id: int) -> bool:
            voice_profile = await self.db.get(VoiceProfileModel, id)

            if not voice_profile:
                return False
    
            return True
