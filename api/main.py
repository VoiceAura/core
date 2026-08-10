from fastapi import FastAPI

app = FastAPI(title="VoiceAura API")


@app.get("/health")
async def health() -> dict:
    """Endpoint de verificacao -- confirma que a API esta viva."""
    return {"status": "ok"}
