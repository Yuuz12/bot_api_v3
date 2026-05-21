from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.db.url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.app_debug,
)

engine_myuz = create_async_engine(
    settings.db_myuz.url,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    echo=settings.app_debug,
)

engine_invitation = create_async_engine(
    settings.db_invitation.url,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    echo=settings.app_debug,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async_session_myuz = async_sessionmaker(engine_myuz, class_=AsyncSession, expire_on_commit=False)
async_session_invitation = async_sessionmaker(engine_invitation, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
