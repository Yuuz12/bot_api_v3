from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Cave(Base):
    __tablename__ = "cave"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qq: Mapped[str] = mapped_column(String(20), nullable=False)
    string: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    time: Mapped[str | None] = mapped_column(String(50), nullable=True)


class CaveRecycle(Base):
    __tablename__ = "cave_recycle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qq: Mapped[str] = mapped_column(String(20), nullable=False)
    string: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    time: Mapped[str | None] = mapped_column(String(50), nullable=True)
