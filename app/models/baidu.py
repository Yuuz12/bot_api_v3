from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class BaiduApplication(Base):
    __tablename__ = "baidu_application"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Appid: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    Expiration: Mapped[str | None] = mapped_column(String(100), nullable=True)
