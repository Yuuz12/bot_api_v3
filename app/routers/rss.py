from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.schemas.rss import RSSSubCreate, BilibiliSubCreate, BilibiliSubUpdate
from app.services.rss_service import RSSService

router = APIRouter()


@router.post("/sub")
async def add_rss_sub(request: RSSSubCreate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.add_rss_sub(db, request.rss_url, request.name, request.sub_group)
    return ResponseBase(data=result)


@router.delete("/sub")
async def delete_rss_sub(uid: str = Query(...), sub_group: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.delete_rss_sub(db, uid, sub_group)
    return ResponseBase(data=result)


@router.put("/sub")
async def update_rss_sub(request: BilibiliSubUpdate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.update_rss_sub(db, request.uid, request.live_status, request.dynamic_upload_time, request.uname, request.roomid)
    return ResponseBase(data=result)


@router.get("/feed")
async def get_rss_feed(url: str = Query(...), key: str = Depends(verify_token)):
    result = await RSSService.get_rss_feed(url)
    return ResponseBase(data=result)


@router.get("/group")
async def get_rss_by_group(group: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.get_rss_by_group(db, group)
    return ResponseBase(data=result)


@router.post("/bilibili/sub")
async def add_bilibili_sub(request: BilibiliSubCreate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.add_bilibili_sub(db, request.uid, request.sub_group, request.uname, request.roomid)
    return ResponseBase(data=result)


@router.delete("/bilibili/sub")
async def delete_bilibili_sub(uid: str = Query(...), sub_group: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.delete_bilibili_sub(db, uid, sub_group)
    return ResponseBase(data=result)


@router.put("/bilibili/sub")
async def update_bilibili_sub(request: BilibiliSubUpdate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await RSSService.update_bilibili_sub(db, request.uid, request.live_status, request.dynamic_upload_time, request.uname, request.roomid)
    return ResponseBase(data=result)
