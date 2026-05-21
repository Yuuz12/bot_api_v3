from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.schemas.statistics import StatisticsUpdate
from app.services.statistics_service import StatisticsService

router = APIRouter()

@router.post("/")
async def update_statistics(request: StatisticsUpdate, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await StatisticsService.update_statistics(db, request.group_id, request.stat_type)
    return ResponseBase(data=result)
