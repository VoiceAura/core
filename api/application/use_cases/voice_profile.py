from domain.errors import NOT_FOUND
from domain.voice_profile_models import CreateVoiceProfile, GetVoiceProfile, VoiceProfile
from domain.ports import VoiceProfileRepository


async def get_voice_profiles_case(
    voice_profile_repository: VoiceProfileRepository,
) -> list[VoiceProfile]:

    return await voice_profile_repository.get_list()

async def get_voice_profile_case(org_id: int, voice_profile_repository: VoiceProfileRepository) -> list[VoiceProfile]:

    return await voice_profile_repository.get_by_organization_id(org_id)

async def create_voice_profile_case(request: CreateVoiceProfile, voice_profile_repository: VoiceProfileRepository) -> VoiceProfile:
    org = await voice_profile_repository.organization_existing(request.organization_id)

    if not org:
        raise NOT_FOUND(detail="Organization not found")

    return await voice_profile_repository.add(request)

async def update_voice_profile_case(id: int, request: CreateVoiceProfile, voice_profile_repository: VoiceProfileRepository) -> VoiceProfile | None:

    org = await voice_profile_repository.organization_existing(request.organization_id)

    if not org:
        raise NOT_FOUND(detail=f"Organization ID: {request.organization_id} not found")
    
    voice_profile = await voice_profile_repository.upgrade(id, request)

    if not voice_profile:
        raise NOT_FOUND(detail="Voice profile not found")

    return voice_profile

async def remove_voice_profile_case(request: GetVoiceProfile, voice_profile_repository: VoiceProfileRepository) -> None:
    voice_profile = await voice_profile_repository.voice_profile_existing(request.id)

    if not voice_profile:
        raise NOT_FOUND(detail="Voice profile not found")

    return await voice_profile_repository.remove(request.id)
