from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from app.dependencies import verify_token
from app.services.storm_service import StormService

router = APIRouter()

@router.get("/text")
async def text_to_image(text: str = Query(...), key: str = Depends(verify_token)):
    buf = StormService.text_to_image(text)
    return StreamingResponse(buf, media_type="image/png")

@router.get("/chaoshi")
async def generate_chaoshi(text: str = Query(...), key: str = Depends(verify_token)):
    buf = StormService.generate_chaoshi(text)
    return StreamingResponse(buf, media_type="image/png")

@router.get("/happy")
async def generate_happy(text: str = Query(...), key: str = Depends(verify_token)):
    buf = StormService.generate_happy(text)
    return StreamingResponse(buf, media_type="image/png")

@router.get("/pw1")
async def generate_pw1(text: str = Query(...), key: str = Depends(verify_token)):
    buf = StormService.generate_pw1(text)
    return StreamingResponse(buf, media_type="image/png")

@router.get("/yesno1")
async def generate_yesno1(a: str = Query(...), b: str = Query(...), key: str = Depends(verify_token)):
    buf = StormService.generate_yesno1(a, b)
    return StreamingResponse(buf, media_type="image/png")
