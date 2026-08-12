import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
  if DATABASE_URL.startswith("postgresql://"):
    database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
	)
