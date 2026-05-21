from sqlalchemy import BigInteger, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class MCBlacklist(Base):
    __tablename__ = "mc_blacklist"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    qq: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    online_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    normal_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class MCBlacklistRecycle(Base):
    __tablename__ = "mc_blacklist_recycle"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    qq: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    online_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    normal_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class MCServer(Base):
    __tablename__ = "minecraft_server"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    qq_group: Mapped[str | None] = mapped_column(String(200), nullable=True)
    host: Mapped[str | None] = mapped_column(String(200), nullable=True)
