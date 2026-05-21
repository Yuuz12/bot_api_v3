from sqlalchemy import BigInteger, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    qq: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="DEFAULT_USER_NAME")
    kook_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    telegram_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    qqguild_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    osu_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    osu_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fst_email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    favorability: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    coin: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    check_in_time_last: Mapped[str | None] = mapped_column(String(50), nullable=True)
    check_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    check_continuous_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    check_rank: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_group: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    registered_time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    registered_timestamp: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    item: Mapped[str | None] = mapped_column(Text, nullable=True)
    badge: Mapped[str | None] = mapped_column(Text, nullable=True)
