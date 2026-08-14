from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.voice import VoiceField, VoiceResponse
from db.Session import get_db
from models.voice import Voice

voice_router = APIRouter(tags=["voices"])

@voice_router.get("/", response_model=List[VoiceResponse])
async def get_voices(db: AsyncSession = Depends(get_db)) -> List[dict]:
  query = select(Voice)
  result = await db.execute(query)
  return result.scalars().all()

@voice_router.get("/{id}", response_model=VoiceResponse)
async def get_voice(id: int, db: AsyncSession = Depends(get_db)) -> dict:
  query = select(Voice).where(Voice.id == id)
  result = await db.execute(query)
  voice = result.scalars().first()

  if not voice:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  return voice

@voice_router.post(
  "/",
  response_model=VoiceResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_voice(voice: VoiceField, db: AsyncSession = Depends(get_db)) -> dict:
  new_voice = Voice(**voice.model_dump())
  db.add(new_voice)
  await db.commit()
  await db.refresh(new_voice)
  return new_voice

@voice_router.put("/{id}", response_model=VoiceResponse)
async def update_voice(
  id: int,
  voice: VoiceField,
  db: AsyncSession = Depends(get_db)
  ) -> dict:

  query = select(Voice).where(Voice.id == id)
  result = await db.execute(query)
  db_voice = result.scalars().first()

  if not db_voice:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  data = voice.model_dump()
  for field, value in data.items():
    setattr(db_voice, field, value)
  await db.commit()
  await db.refresh(db_voice)
  return db_voice

@voice_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice(id: int, db: AsyncSession = Depends(get_db)) -> None:
  query = select(Voice).where(Voice.id == id)
  result = await db.execute(query)
  voice = result.scalars().first()

  if not voice:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  await db.delete(voice)
  await db.commit()
  return None
