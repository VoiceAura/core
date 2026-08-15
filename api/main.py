from fastapi import FastAPI

from db.Session import get_db
from routers.organization import router as organization_router
from routers.user import router as user_router
from routers.voice_profile import router as voice_profile_router
from routers.voice_sample import router as voice_sample_router

app = FastAPI(
    title="VoiceAura API",
    version="0.0.1"
  )
router_list = [
                organization_router,
                user_router,
                voice_profile_router,
                voice_sample_router
                ]

get_db()

@app.get("/health")
async def health() -> dict:  # type: ignore
    """Endpoint de verificacao -- confirma que a API esta viva."""
    return {"status": "ok"} # type: ignore

for router in router_list:
    app.include_router(router)

