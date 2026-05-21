from fastapi import APIRouter, Depends, Query
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
import httpx

router = APIRouter()

@router.post("/search")
async def search_subjects(keyword: str = Query(...), type: int = Query(2), limit: int = Query(10), offset: int = Query(0), key: str = Depends(verify_token)):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.bgm.tv/v0/search/subjects",
            headers={"User-Agent": "Yuuz12/sub_Bangumi"},
            json={"keyword": keyword, "filter": {"type": [type]}, "limit": limit, "offset": offset},
        )
        response.raise_for_status()
        return ResponseBase(data=response.json())
