from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from app.models.minecraft import MCBlacklist, MCBlacklistRecycle, MCServer
from app.exceptions import NotFoundError, BadRequestError, ConflictError


class MinecraftService:
    @staticmethod
    async def add_to_blacklist(db: AsyncSession, qq: str, email: str | None, online_id: str | None, normal_id: str | None, reason: str | None) -> dict:
        result = await db.execute(select(MCBlacklist).where(MCBlacklist.qq == qq))
        if result.scalar_one_or_none():
            raise ConflictError("该QQ号已在黑名单中")
        entry = MCBlacklist(qq=qq, email=email, online_id=online_id, normal_id=normal_id, reason=reason)
        db.add(entry)
        await db.flush()
        return {"id": entry.id, "qq": entry.qq, "email": entry.email, "online_id": entry.online_id, "normal_id": entry.normal_id, "reason": entry.reason}

    @staticmethod
    async def get_blacklist_user(db: AsyncSession, qq: str) -> dict:
        result = await db.execute(select(MCBlacklist).where(MCBlacklist.qq == qq))
        entry = result.scalar_one_or_none()
        if not entry:
            raise NotFoundError("黑名单中未找到该用户")
        return {"id": entry.id, "qq": entry.qq, "email": entry.email, "online_id": entry.online_id, "normal_id": entry.normal_id, "reason": entry.reason}

    @staticmethod
    async def remove_from_blacklist(db: AsyncSession, delete_type: int, qq: str | None = None, entry_id: int | None = None) -> dict:
        if delete_type == 1 and qq:
            result = await db.execute(select(MCBlacklist).where(MCBlacklist.qq == qq))
        elif delete_type == 2 and entry_id:
            result = await db.execute(select(MCBlacklist).where(MCBlacklist.id == entry_id))
        else:
            raise BadRequestError("参数错误")
        entry = result.scalar_one_or_none()
        if not entry:
            raise NotFoundError("黑名单中未找到该记录")
        recycle = MCBlacklistRecycle(id=entry.id, qq=entry.qq, email=entry.email, online_id=entry.online_id, normal_id=entry.normal_id, reason=entry.reason)
        db.add(recycle)
        await db.delete(entry)
        await db.flush()
        return {"id": recycle.id, "qq": recycle.qq, "status": "deleted_and_recycled"}

    @staticmethod
    async def get_server_by_name(db: AsyncSession, name: str) -> list:
        result = await db.execute(select(MCServer).where(func.find_in_set(name, MCServer.name) > 0))
        servers = result.scalars().all()
        return [{"id": s.id, "name": s.name, "qq_group": s.qq_group, "host": s.host} for s in servers]

    @staticmethod
    async def get_server_by_group(db: AsyncSession, qq_group: str) -> list:
        result = await db.execute(select(MCServer).where(func.find_in_set(qq_group, MCServer.qq_group) > 0))
        servers = result.scalars().all()
        return [{"id": s.id, "name": s.name, "qq_group": s.qq_group, "host": s.host} for s in servers]

    @staticmethod
    async def ping_server(ip: str, port: int = 25565) -> dict:
        from mcstatus import JavaServer
        server = JavaServer.lookup(f"{ip}:{port}")
        status = server.status()
        return {
            "ip": ip,
            "port": port,
            "version": status.version.name,
            "protocol": status.version.protocol,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "motd": str(status.description),
            "latency": status.latency,
        }
