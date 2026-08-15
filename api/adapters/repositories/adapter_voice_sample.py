from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import VoiceSampleRepository
from domain.voice_sample_models import CreateVoiceSample, VoiceSample
from models.voice_sample import VoiceSampleModel
from models.voice_profile import VoiceProfileModel


class AdapterVoiceSample(VoiceSampleRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_list(self) -> list[VoiceSample]:
        query = select(VoiceSampleModel)
        result = await self.db.execute(query)
        voice_samples = result.scalars().all()

        return [
                VoiceSample(
                    id=voice_sample.id,
                    voice_profile_id=voice_sample.voice_profile_id,
                    storage_reference=voice_sample.storage_reference,
                    duration=voice_sample.duration,
                    format=voice_sample.format,
                    created_at=voice_sample.created_at
                )
                for voice_sample in voice_samples
            ]

    async def get_by_voice_profile_id(self, voice_profile_id: int) -> list[VoiceSample]:
        query = select(VoiceSampleModel).where(
                            VoiceSampleModel.voice_profile_id == voice_profile_id
                        )
        result = await self.db.execute(query)
        voice_samples = result.scalars().all()

        return [
                VoiceSample(
                    id=voice_sample.id,
                    voice_profile_id=voice_sample.voice_profile_id,
                    storage_reference=voice_sample.storage_reference,
                    duration=voice_sample.duration,
                    format=voice_sample.format,
                    created_at=voice_sample.created_at
                )
                for voice_sample in voice_samples
            ]

    async def add(self, request: CreateVoiceSample) -> VoiceSample:
            db_voice_sample = VoiceSampleModel(
                voice_profile_id=request.voice_profile_id,
                storage_reference=request.storage_reference,
                duration=request.duration,
                format=request.format
            )

            self.db.add(db_voice_sample)
            await self.db.commit()
            await self.db.refresh(db_voice_sample)

            return VoiceSample(
                id=db_voice_sample.id,
                voice_profile_id=db_voice_sample.voice_profile_id,
                storage_reference=db_voice_sample.storage_reference,
                duration=db_voice_sample.duration,
                format=db_voice_sample.format,
                created_at=db_voice_sample.created_at
            )
          

    async def upgrade(self, id: int, request: CreateVoiceSample) -> VoiceSample | None:
        db_voice_sample = await self.db.get(VoiceSampleModel, id)
        if not db_voice_sample:
            return None

        db_voice_sample.voice_profile_id = request.voice_profile_id
        db_voice_sample.storage_reference = request.storage_reference
        db_voice_sample.duration = request.duration
        db_voice_sample.format = request.format 

        await self.db.commit()
        await self.db.refresh(db_voice_sample)

        return VoiceSample(
            id=db_voice_sample.id,
            voice_profile_id=db_voice_sample.voice_profile_id,
            storage_reference=db_voice_sample.storage_reference,
            duration=db_voice_sample.duration,
            format=db_voice_sample.format,
            created_at=db_voice_sample.created_at
        )
            
    async def remove(self, id: int) -> None:
        query = select(VoiceSampleModel).where(VoiceSampleModel.id == id)
        result = await self.db.execute(query)
        voice_sample = result.scalar_one_or_none()

        if not voice_sample:
            return

        await self.db.delete(voice_sample)
        return await self.db.commit()

    async def voice_profile_existing(self, id: int) -> bool:
        voice_profile = await self.db.get(VoiceProfileModel, id)

        if not voice_profile:
            return False

        return True

    async def voice_sample_existing(self, id: int) -> bool:
        voice_sample = await self.db.get(VoiceSampleModel, id)

        if not voice_sample:
            return False

        return True