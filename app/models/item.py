from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    cost_coin: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_favorability: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    need_favorability: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
