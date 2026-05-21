from sqlalchemy import BigInteger, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Prize(Base):
    __tablename__ = "Prize"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    coin: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


class PrizeUser(Base):
    __tablename__ = "Prize_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qq: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    coin: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_time_attended: Mapped[str | None] = mapped_column(String(50), nullable=True)
