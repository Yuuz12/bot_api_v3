from fastapi import APIRouter, Depends, Query
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
import httpx

router = APIRouter()

@router.get("/info")
async def get_doujinshi_info(id: int = Query(...), key: str = Depends(verify_token)):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"https://nhentai.xxx/g/{id}")
        return ResponseBase(data={"id": id, "url": f"https://nhentai.xxx/g/{id}"})

@router.get("/search")
async def search_doujinshi(query: str = Query(...), page: int = Query(1), key: str = Depends(verify_token)):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"https://nhentai.xxx/api/galleries/search", params={"query": query, "page": page})
        return ResponseBase(data=response.json())
