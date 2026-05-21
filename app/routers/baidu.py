from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.models.baidu import BaiduApplication
from app.config import settings
import httpx
import time

router = APIRouter()

@router.post("/img-censor")
async def img_censor(img: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BaiduApplication).limit(1))
    app = result.scalars().first()
    if not app:
        return ResponseBase(code=500, message="百度应用未配置")

    current_time = int(time.time())
    if not app.Access_token or not app.Expiration:
        need_refresh = True
    else:
        try:
            from datetime import datetime
            expiration = datetime.strptime(app.Expiration, "%Y-%m-%d %H:%M:%S")
            need_refresh = (expiration.timestamp() - current_time) < 86400
        except Exception:
            need_refresh = True

    if need_refresh:
        async with httpx.AsyncClient(timeout=30.0) as client:
            token_response = await client.post(
                "https://aip.baidubce.com/oauth/2.0/token",
                params={
                    "grant_type": "client_credentials",
                    "client_id": settings.baidu.client_id,
                    "client_secret": settings.baidu.client_secret,
                },
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token", "")
            expires_in = token_data.get("expires_in", 2592000)
            from datetime import datetime, timedelta
            expiration = datetime.now() + timedelta(seconds=expires_in)
            app.Access_token = access_token
            app.Expiration = expiration.strftime("%Y-%m-%d %H:%M:%S")
            await db.flush()

    async with httpx.AsyncClient(timeout=30.0) as client:
        censor_response = await client.post(
            "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined",
            params={"access_token": app.Access_token},
            data={"img": img},
        )
        return ResponseBase(data=censor_response.json())
