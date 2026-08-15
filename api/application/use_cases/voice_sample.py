from domain.errors import NOT_FOUND
from domain.voice_sample_models import CreateVoiceSample, GetVoiceSample, VoiceSample
from domain.ports import VoiceSampleRepository


async def get_voice_samples_case(
    voice_sample_repository: VoiceSampleRepository,
) -> list[VoiceSample]:

    return await voice_sample_repository.get_list()

async def get_voice_samples_by_profile_id_case(voice_profile_id: int, voice_sample_repository: VoiceSampleRepository) -> list[VoiceSample]:

    return await voice_sample_repository.get_by_voice_profile_id(voice_profile_id)

async def create_voice_sample_case(request: CreateVoiceSample, voice_sample_repository: VoiceSampleRepository) -> VoiceSample:
    org = await voice_sample_repository.voice_profile_existing(request.voice_profile_id)

    if not org:
        raise NOT_FOUND(detail="Voice profile not found")

    return await voice_sample_repository.add(request)

async def update_voice_sample_case(id: int, request: CreateVoiceSample, voice_sample_repository: VoiceSampleRepository) -> VoiceSample | None:

    org = await voice_sample_repository.voice_profile_existing(request.voice_profile_id)

    if not org:
        raise NOT_FOUND(detail=f"Voice profile ID: {request.voice_profile_id} not found")
    
    voice_sample = await voice_sample_repository.upgrade(id, request)

    if not voice_sample:
        raise NOT_FOUND(detail="Voice sample not found")

    return voice_sample

async def remove_voice_sample_case(request: GetVoiceSample, voice_sample_repository: VoiceSampleRepository) -> None:
    voice_sample = await voice_sample_repository.voice_sample_existing(request.id)

    if not voice_sample:
        raise NOT_FOUND(detail="Voice sample not found")

    return await voice_sample_repository.remove(request.id)
