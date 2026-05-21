import time
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.moauth import MOAuth
from app.exceptions import NotFoundError, BadRequestError, ConflictError


class MOAuthService:
    @staticmethod
    async def get_moauth(db: AsyncSession, qq: str) -> dict:
        result = await db.execute(select(MOAuth).where(MOAuth.qq == qq))
        entry = result.scalar_one_or_none()
        if not entry:
            raise NotFoundError("未找到MOAuth记录")
        return {"id": entry.id, "qq": entry.qq, "kook_id": entry.kook_id, "name": entry.name, "status": entry.status, "timestamp": entry.timestamp}

    @staticmethod
    async def create_moauth(db: AsyncSession, qq: str, kook_id: str, name: str) -> dict:
        result = await db.execute(select(MOAuth).where(MOAuth.qq == qq).order_by(MOAuth.id.desc()))
        existing = result.scalar_one_or_none()
        if existing and existing.timestamp and existing.timestamp + 300 > int(time.time()):
            raise BadRequestError("请求过于频繁，请5分钟后再试")
        code = "".join(secrets.choice("0123456789") for _ in range(6))
        now = int(time.time())
        entry = MOAuth(qq=qq, kook_id=kook_id, name=name, moauth=code, status=0, time=str(now), timestamp=now)
        db.add(entry)
        await db.flush()
        return {"id": entry.id, "qq": entry.qq, "moauth": code, "status": entry.status}

    @staticmethod
    async def bind_kook(db: AsyncSession, qq: str, key: str) -> dict:
        result = await db.execute(select(MOAuth).where(MOAuth.qq == qq).order_by(MOAuth.id.desc()))
        entry = result.scalar_one_or_none()
        if not entry:
            raise NotFoundError("未找到MOAuth记录")
        if entry.status == 1:
            raise BadRequestError("已绑定")
        if entry.moauth != key:
            raise BadRequestError("验证码错误")
        entry.status = 1
        await db.flush()
        return {"qq": entry.qq, "kook_id": entry.kook_id, "status": "bound"}
