from fastapi import FastAPI
from db.Session import get_db
from routers.voice import voice_router
from routers.organization import organization_router
from routers.user import user_router

app = FastAPI(title="VoiceAura API")

get_db()

@app.get("/health")
async def health() -> dict:
  """Endpoint de verificacao -- confirma que a API esta viva."""
  return {"status": "ok"}

app.include_router(voice_router, prefix="/voices")
app.include_router(organization_router, prefix="/organizations")
app.include_router(user_router, prefix="/users")
