from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.adapter_voice_sample import AdapterVoiceSample
from domain.voice_sample_models import CreateVoiceSample, GetVoiceSample
from schemas.voice_sample import VoiceSampleResponse
from application.use_cases.voice_sample import (create_voice_sample_case, get_voice_samples_by_profile_id_case,
                                        get_voice_samples_case, remove_voice_sample_case)

from db.Session import get_db
from utils.response_util import to_response
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(
    prefix="/voice-samples",
    tags=["voice-sample"]
    )

@router.get("/", response_model=list[VoiceSampleResponse])
async def get_voice_samples(db: AsyncSession = Depends(get_db)) -> list[VoiceSampleResponse]:
    adapter = AdapterVoiceSample(db)
    result = await get_voice_samples_case(adapter)

    return [
      to_response(VoiceSampleResponse, voice_sample)
      for voice_sample in result
    ]

@router.get("/{voice_profile_id}/samples", response_model=list[VoiceSampleResponse])
async def get_voice_sample(voice_profile_id: int, db: AsyncSession = Depends(get_db)) -> list[VoiceSampleResponse]:
    adapter = AdapterVoiceSample(db)
    result = await get_voice_samples_by_profile_id_case(voice_profile_id, adapter)
  
    return  [
      to_response(VoiceSampleResponse, voice_sample)
      for voice_sample in result
    ]

@router.post(
    "/{voice_profile_id}/samples",
    response_model=VoiceSampleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_voice_sample(
    voice_profile_id: int,
    file: UploadFile = File(...),
    duration: float = Form(...),
    db: AsyncSession = Depends(get_db),
) -> VoiceSampleResponse:

    adapter = AdapterVoiceSample(db)

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(file.file.read())

    request = CreateVoiceSample(
        voice_profile_id=voice_profile_id,
        storage_reference=f"/uploads/{file.filename}",
        duration=duration,
        format=file.content_type or "",
    )

    result = await create_voice_sample_case(
        request,
        adapter,
    )

    return to_response(VoiceSampleResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice_sample(id: int, db: AsyncSession = Depends(get_db)) -> None:
  adapter = AdapterVoiceSample(db)
  request = GetVoiceSample(id=id)
  
  return await remove_voice_sample_case(request, adapter)
