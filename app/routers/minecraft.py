from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.schemas.minecraft import MCBlacklistCreate, MCBlacklistDelete, MCPingRequest
from app.services.minecraft_service import MinecraftService

router = APIRouter()


@router.post("/blacklist")
async def add_to_blacklist(request: MCBlacklistCreate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MinecraftService.add_to_blacklist(db, request.qq, request.email, request.online_id, request.normal_id, request.reason)
    return ResponseBase(data=result)


@router.get("/blacklist/{qq}")
async def get_blacklist_user(qq: str, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MinecraftService.get_blacklist_user(db, qq)
    return ResponseBase(data=result)


@router.delete("/blacklist")
async def remove_from_blacklist(request: MCBlacklistDelete, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MinecraftService.remove_from_blacklist(db, request.type, request.qq, request.id)
    return ResponseBase(data=result)


@router.get("/server")
async def get_server_by_name(name: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MinecraftService.get_server_by_name(db, name)
    return ResponseBase(data=result)


@router.get("/server/by-group")
async def get_server_by_group(qq_group: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MinecraftService.get_server_by_group(db, qq_group)
    return ResponseBase(data=result)


@router.get("/ping")
async def ping_server(ip: str = Query(...), port: int = Query(25565), key: str = Depends(verify_token)):
    result = await MinecraftService.ping_server(ip, port)
    return ResponseBase(data=result)
