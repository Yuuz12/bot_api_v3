from sqlalchemy import Integer, String, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class InvitationCode(Base):
    __tablename__ = "invitation_codes"
    __table_args__ = {"schema": None}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str | None] = mapped_column(String(100), nullable=True)


class InvitationQQ(Base):
    __tablename__ = "invitation_qq"
    __table_args__ = {"schema": None}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qq: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    codes: Mapped[str | None] = mapped_column(String(100), nullable=True)
    time: Mapped[str | None] = mapped_column(String(50), nullable=True)


class InvitationNumber(Base):
    __tablename__ = "invitation_number"
    __table_args__ = {"schema": None}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
