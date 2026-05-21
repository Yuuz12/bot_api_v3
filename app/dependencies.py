from typing import AsyncGenerator

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, async_session_myuz, async_session_invitation
from app.exceptions import AuthError
from app.models.auth import AuthKey
from app.config import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db_myuz() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_myuz() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db_invitation() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_invitation() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def verify_token(key: str = Query(..., alias="key")) -> str:
    if not key:
        raise AuthError("缺少鉴权参数")
    if key in settings.auth_tokens:
        return key
    async with async_session() as session:
        result = await session.execute(
            AuthKey.__table__.select().where(AuthKey.token == key)
        )
        if result.first() is not None:
            return key
    raise AuthError("无效的鉴权令牌")
