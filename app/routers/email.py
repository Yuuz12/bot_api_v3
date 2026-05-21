from fastapi import APIRouter, Depends
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
from app.schemas.email import EmailSendRequest
from app.services.email_service import EmailService

router = APIRouter()

@router.post("/kirino")
async def send_email_kirino(request: EmailSendRequest, key: str = Depends(verify_token)):
    to = request.qq + "@qq.com" if "@" not in request.qq else request.qq
    result = await EmailService.send_email(to, request.subject, request.body, "kirino")
    return ResponseBase(data=result)

@router.post("/shiruku")
async def send_email_shiruku(request: EmailSendRequest, key: str = Depends(verify_token)):
    to = request.qq + "@qq.com" if "@" not in request.qq else request.qq
    result = await EmailService.send_email(to, request.subject, request.body, "shiruku")
    return ResponseBase(data=result)
