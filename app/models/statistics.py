from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
