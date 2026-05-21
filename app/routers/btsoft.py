from fastapi import APIRouter, Depends
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
from app.services.btsoft_service import BtSoftService

router = APIRouter()

@router.get("/system-info")
async def get_system_info(key: str = Depends(verify_token)):
    result = await BtSoftService.get_system_info()
    return ResponseBase(data=result)

@router.post("/re-memory")
async def re_memory(key: str = Depends(verify_token)):
    result = await BtSoftService.re_memory()
    return ResponseBase(data=result)
