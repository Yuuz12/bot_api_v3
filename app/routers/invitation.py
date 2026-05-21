from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db_invitation, verify_token
from app.schemas.common import ResponseBase
from app.schemas.invitation import InvitationObtainRequest, InvitationQueryRequest
from app.services.invitation_service import InvitationService

router = APIRouter()

@router.post("/obtain")
async def obtain_invitation_code(request: InvitationObtainRequest, key: str = Depends(verify_token), db: AsyncSession = Depends(get_db_invitation)):
    result = await InvitationService.obtain_invitation_code(db, request.qq)
    return ResponseBase(data=result)

@router.get("/query")
async def query_invitation_code(qq: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db_invitation)):
    result = await InvitationService.query_invitation_code(db, qq)
    return ResponseBase(data=result)
