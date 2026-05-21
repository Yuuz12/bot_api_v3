from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class MOAuth(Base):
    __tablename__ = "MOAuth"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qq: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    kook_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    moauth: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[int | None] = mapped_column(Integer, nullable=True)
