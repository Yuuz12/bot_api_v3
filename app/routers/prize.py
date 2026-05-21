from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.services.prize_service import PrizeService
from app.schemas.prize import PrizeDrawRequest, PrizeCoinRankRequest

router = APIRouter()

@router.get("/coin")
async def get_prize_coin(key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await PrizeService.get_prize_coin(db)
    return ResponseBase(data=result)

@router.get("/coin/rank")
async def get_prize_coin_rank(request: PrizeCoinRankRequest = Depends(), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await PrizeService.get_prize_coin_rank(db, request.quantity)
    return ResponseBase(data=result)

@router.post("/draw")
async def draw_prize(request: PrizeDrawRequest, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await PrizeService.draw_prize(db, request.qq, request.coin, request.type)
    return ResponseBase(data=result)
