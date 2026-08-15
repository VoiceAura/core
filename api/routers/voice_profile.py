from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.adapter_voice_profile import AdapterVoiceProfile
from application.use_cases.voice_profile import (create_voice_profile_case, get_voice_profile_case,
                                        get_voice_profiles_case, remove_voice_profile_case,
                                        update_voice_profile_case)
from db.Session import get_db
from domain.voice_profile_models import CreateVoiceProfile, GetVoiceProfile
from schemas.voice_profile import VoiceProfileField, VoiceProfileResponse
from utils.response_util import to_response

router = APIRouter(
    prefix="/voice-profiles",
    tags=["voice-profile"]
    )

@router.get("/", response_model=list[VoiceProfileResponse])
async def get_voice_profiles(db: AsyncSession = Depends(get_db)) -> list[VoiceProfileResponse]:
    adapter = AdapterVoiceProfile(db)
    result = await get_voice_profiles_case(adapter)

    return [
      to_response(VoiceProfileResponse, voice_profile)
      for voice_profile in result
    ]

@router.get("/{org_id}", response_model=list[VoiceProfileResponse])
async def get_voice_profile(org_id: int, db: AsyncSession = Depends(get_db)) -> list[VoiceProfileResponse]:
    adapter = AdapterVoiceProfile(db)
    result = await get_voice_profile_case(org_id, adapter)
  
    return  [
      to_response(VoiceProfileResponse, voice_profile)
      for voice_profile in result
    ]

@router.post(
  "/",
  response_model=VoiceProfileResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_voice_profile(voice_profile: VoiceProfileField, db: AsyncSession = Depends(get_db)) -> VoiceProfileResponse:
    adapter = AdapterVoiceProfile(db)
    request = CreateVoiceProfile(organization_id=voice_profile.organization_id,
                         name=voice_profile.name,
                         provider=voice_profile.provider,
                         provider_voice_id=voice_profile.provider_voice_id,
                         status=voice_profile.status)
    result = await create_voice_profile_case(request, adapter)
    return to_response(VoiceProfileResponse, result)

@router.put("/{id}", response_model=VoiceProfileResponse)
async def update_voice_profile(
    id: int,
    voice_profile: VoiceProfileField,
    db: AsyncSession = Depends(get_db)
) -> VoiceProfileResponse:
    adapter = AdapterVoiceProfile(db)
    request = CreateVoiceProfile(organization_id=voice_profile.organization_id,
                             name=voice_profile.name,
                             provider=voice_profile.provider,
                             provider_voice_id=voice_profile.provider_voice_id,
                             status=voice_profile.status)
    result = await update_voice_profile_case(id, request, adapter)
    return to_response(VoiceProfileResponse, result)
   

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice_profile(id: int, db: AsyncSession = Depends(get_db)) -> None:
  adapter = AdapterVoiceProfile(db)
  request = GetVoiceProfile(id=id)
  
  return await remove_voice_profile_case(request, adapter)
