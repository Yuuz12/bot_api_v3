from sqlalchemy import BigInteger, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class BilibiliSub(Base):
    __tablename__ = "bilibili_sub"

    uid: Mapped[str] = mapped_column(String(20), primary_key=True)
    sub_group: Mapped[str | None] = mapped_column(Text, nullable=True)
    live_status: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    dynamic_upload_time: Mapped[str | None] = mapped_column(String(100), nullable=True)
    uname: Mapped[str | None] = mapped_column(String(200), nullable=True)
    roomid: Mapped[int | None] = mapped_column(BigInteger, nullable=True)


class RSSSub(Base):
    __tablename__ = "RSS_sub"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sub_group: Mapped[str | None] = mapped_column(Text, nullable=True)
    pub_upload_time: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rss_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
