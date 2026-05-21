from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.schemas.moauth import MOAuthCreate, MOAuthBindKook
from app.services.moauth_service import MOAuthService

router = APIRouter()


@router.get("/")
async def get_moauth(qq: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MOAuthService.get_moauth(db, qq)
    return ResponseBase(data=result)


@router.post("/")
async def create_moauth(request: MOAuthCreate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MOAuthService.create_moauth(db, request.qq, request.kook_id, request.name)
    return ResponseBase(data=result)


@router.get("/bind-kook")
async def bind_kook(qq: str = Query(...), key: str = Query(..., alias="key"), auth_key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await MOAuthService.bind_kook(db, qq, key)
    return ResponseBase(data=result)
