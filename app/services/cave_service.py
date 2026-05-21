import asyncio
import ipaddress
import socket
from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.models.cave import Cave, CaveRecycle
from app.utils.http import async_get_raw


class CaveService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cave(self, type: int, qq: str, string: str | None, image: str | None) -> Cave:
        cave = Cave(
            type=type,
            qq=qq,
            string=string,
            image=image,
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.db.add(cave)
        await self.db.flush()
        return cave

    async def get_random_cave(self) -> Cave:
        max_id_subq = select(func.max(Cave.id)).scalar_subquery()
        stmt = (
            select(Cave)
            .where(Cave.id >= func.floor(func.rand() * max_id_subq))
            .order_by(Cave.id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        cave = result.scalar_one_or_none()
        if cave is None:
            raise NotFoundError("回声洞为空")
        return cave

    async def get_cave_by_id(self, cave_id: int) -> Cave:
        stmt = select(Cave).where(Cave.id == cave_id)
        result = await self.db.execute(stmt)
        cave = result.scalar_one_or_none()
        if cave is None:
            raise NotFoundError("回声洞不存在")
        return cave

    async def update_cave(
        self,
        cave_id: int,
        qq: str,
        type: int | None,
        string: str | None,
        image: str | None,
        user_group: int,
    ) -> Cave:
        cave = await self.get_cave_by_id(cave_id)
        if user_group != 52 and cave.qq != qq:
            raise ForbiddenError("只能修改自己发布的回声洞")
        if type is not None:
            cave.type = type
        if string is not None:
            cave.string = string
        if image is not None:
            cave.image = image
        await self.db.flush()
        return cave

    async def delete_cave(self, cave_id: int) -> None:
        cave = await self.get_cave_by_id(cave_id)
        recycle = CaveRecycle(
            id=cave.id,
            type=cave.type,
            qq=cave.qq,
            string=cave.string,
            image=cave.image,
            time=cave.time,
        )
        self.db.add(recycle)
        await self.db.delete(cave)
        await self.db.flush()

    async def recover_cave(self, cave_id: int) -> Cave:
        stmt = select(CaveRecycle).where(CaveRecycle.id == cave_id)
        result = await self.db.execute(stmt)
        recycle = result.scalar_one_or_none()
        if recycle is None:
            raise NotFoundError("回收站中不存在该回声洞")
        cave = Cave(
            id=recycle.id,
            type=recycle.type,
            qq=recycle.qq,
            string=recycle.string,
            image=recycle.image,
            time=recycle.time,
        )
        self.db.add(cave)
        await self.db.delete(recycle)
        await self.db.flush()
        return cave

    async def search_cave(self, keywords: str) -> list[Cave]:
        pattern = f"%{keywords}%"
        stmt = select(Cave).where(Cave.string.like(pattern))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def upload_image(self, url: str) -> bytes:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            raise BadRequestError("无效的URL")
        if not parsed.scheme or parsed.scheme not in ("http", "https"):
            raise BadRequestError("仅支持HTTP/HTTPS协议")
        try:
            addr_info = await asyncio.to_thread(socket.getaddrinfo, hostname, None)
        except socket.gaierror:
            raise BadRequestError("无法解析域名")
        for info in addr_info:
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local or ip.is_unspecified:
                raise BadRequestError("不允许访问内网地址")
        try:
            return await async_get_raw(url)
        except Exception:
            raise BadRequestError("图片下载失败")
