from fastapi import APIRouter, Depends, Query
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
from app.services.osu_service import OsuService

router = APIRouter()

@router.get("/scoreboard")
async def get_scoreboard(username: str = Query(...), mode: str = Query("osu"), key: str = Depends(verify_token)):
    result = await OsuService.get_scoreboard(username, mode)
    return ResponseBase(data=result)

@router.get("/signature")
async def get_signature(username: str = Query(...), mode: str = Query("osu"), key: str = Depends(verify_token)):
    result = await OsuService.get_signature(username, mode)
    return ResponseBase(data=result)
