from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.rss import RSSSub, BilibiliSub
from app.exceptions import NotFoundError, BadRequestError, ConflictError
import feedparser
import httpx


class RSSService:
    @staticmethod
    async def add_rss_sub(db: AsyncSession, rss_url: str, name: str, sub_group: str) -> dict:
        sub = RSSSub(rss_url=rss_url, name=name, sub_group=sub_group)
        db.add(sub)
        await db.flush()
        return {"id": sub.id, "rss_url": sub.rss_url, "name": sub.name, "sub_group": sub.sub_group}

    @staticmethod
    async def delete_rss_sub(db: AsyncSession, uid: str, sub_group: str) -> dict:
        result = await db.execute(select(BilibiliSub).where(BilibiliSub.uid == uid))
        sub = result.scalar_one_or_none()
        if not sub:
            raise NotFoundError("订阅不存在")
        groups = sub.sub_group.split(",") if sub.sub_group else []
        if sub_group in groups:
            groups.remove(sub_group)
        if not groups:
            await db.delete(sub)
            return {"uid": uid, "status": "deleted"}
        else:
            sub.sub_group = ",".join(groups)
            await db.flush()
            return {"uid": uid, "sub_group": sub.sub_group, "status": "updated"}

    @staticmethod
    async def update_rss_sub(db: AsyncSession, uid: str, live_status: int | None = None, dynamic_upload_time: str | None = None, uname: str | None = None, roomid: int | None = None) -> dict:
        result = await db.execute(select(BilibiliSub).where(BilibiliSub.uid == uid))
        sub = result.scalar_one_or_none()
        if not sub:
            raise NotFoundError("订阅不存在")
        if live_status is not None:
            sub.live_status = live_status
        if dynamic_upload_time is not None:
            sub.dynamic_upload_time = dynamic_upload_time
        if uname is not None:
            sub.uname = uname
        if roomid is not None:
            sub.roomid = roomid
        await db.flush()
        return {"uid": sub.uid, "uname": sub.uname, "live_status": sub.live_status}

    @staticmethod
    async def get_rss_feed(url: str) -> list:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
        feed = feedparser.parse(response.text)
        entries = []
        for entry in feed.entries[:10]:
            entries.append({
                "title": getattr(entry, "title", ""),
                "link": getattr(entry, "link", ""),
                "published": getattr(entry, "published", ""),
                "summary": getattr(entry, "summary", ""),
            })
        return entries

    @staticmethod
    async def get_rss_by_group(db: AsyncSession, group: str) -> list:
        result = await db.execute(select(RSSSub).where(func.find_in_set(group, RSSSub.sub_group) > 0))
        subs = result.scalars().all()
        return [{"id": s.id, "name": s.name, "rss_url": s.rss_url, "sub_group": s.sub_group} for s in subs]

    @staticmethod
    async def add_bilibili_sub(db: AsyncSession, uid: str, sub_group: str, uname: str | None = None, roomid: int | None = None) -> dict:
        result = await db.execute(select(BilibiliSub).where(BilibiliSub.uid == uid))
        sub = result.scalar_one_or_none()
        if sub:
            groups = sub.sub_group.split(",") if sub.sub_group else []
            if sub_group not in groups:
                groups.append(sub_group)
            sub.sub_group = ",".join(groups)
            await db.flush()
            return {"uid": sub.uid, "sub_group": sub.sub_group, "status": "updated"}
        sub = BilibiliSub(uid=uid, sub_group=sub_group, uname=uname, roomid=roomid)
        db.add(sub)
        await db.flush()
        return {"uid": sub.uid, "sub_group": sub.sub_group, "status": "created"}

    @staticmethod
    async def delete_bilibili_sub(db: AsyncSession, uid: str, sub_group: str) -> dict:
        return await RSSService.delete_rss_sub(db, uid, sub_group)

    @staticmethod
    async def update_bilibili_sub(db: AsyncSession, uid: str, live_status: int | None = None, dynamic_upload_time: str | None = None, uname: str | None = None, roomid: int | None = None) -> dict:
        return await RSSService.update_rss_sub(db, uid, live_status, dynamic_upload_time, uname, roomid)
