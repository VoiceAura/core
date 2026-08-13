from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import  Mapped, mapped_column
from db.Base import Base


class Voice(Base):
  __tablename__ = "voices"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  embedding_path: Mapped[str | None] = mapped_column(String(500))
  cliente_id: Mapped[int] 
  created_at: Mapped[datetime] = mapped_column(
                     DateTime(timezone=True),
                     default=lambda: datetime.now()
                     )
