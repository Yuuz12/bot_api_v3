import base64

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, verify_token
from app.services.cave_service import CaveService

router = APIRouter()


class CaveCreateRequest(BaseModel):
    type: int = 0
    qq: str
    string: str | None = None
    image: str | None = None


class CaveUpdateRequest(BaseModel):
    qq: str
    type: int | None = None
    string: str | None = None
    image: str | None = None
    user_group: int = 0


class ImageUploadRequest(BaseModel):
    url: str


def _cave_to_dict(cave) -> dict:
    return {
        "id": cave.id,
        "type": cave.type,
        "qq": cave.qq,
        "string": cave.string,
        "image": cave.image,
        "time": cave.time,
    }


@router.post("/")
async def create_cave(
    body: CaveCreateRequest,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    cave = await service.create_cave(type=body.type, qq=body.qq, string=body.string, image=body.image)
    return {"code": 200, "message": "success", "data": _cave_to_dict(cave)}


@router.get("/random")
async def get_random_cave(
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    cave = await service.get_random_cave()
    return {"code": 200, "message": "success", "data": _cave_to_dict(cave)}


@router.get("/search")
async def search_cave(
    keywords: str = Query(...),
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    caves = await service.search_cave(keywords)
    return {"code": 200, "message": "success", "data": [_cave_to_dict(c) for c in caves]}


@router.post("/upload-image")
async def upload_image(
    body: ImageUploadRequest,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    image_bytes = await service.upload_image(body.url)
    return {"code": 200, "message": "success", "data": base64.b64encode(image_bytes).decode()}


@router.get("/{cave_id}")
async def get_cave_by_id(
    cave_id: int,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    cave = await service.get_cave_by_id(cave_id)
    return {"code": 200, "message": "success", "data": _cave_to_dict(cave)}


@router.put("/{cave_id}")
async def update_cave(
    cave_id: int,
    body: CaveUpdateRequest,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    cave = await service.update_cave(
        cave_id=cave_id,
        qq=body.qq,
        type=body.type,
        string=body.string,
        image=body.image,
        user_group=body.user_group,
    )
    return {"code": 200, "message": "success", "data": _cave_to_dict(cave)}


@router.delete("/{cave_id}")
async def delete_cave(
    cave_id: int,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    await service.delete_cave(cave_id)
    return {"code": 200, "message": "success", "data": None}


@router.post("/{cave_id}/recover")
async def recover_cave(
    cave_id: int,
    db: AsyncSession = Depends(get_db),
    key: str = Depends(verify_token),
):
    service = CaveService(db)
    cave = await service.recover_cave(cave_id)
    return {"code": 200, "message": "success", "data": _cave_to_dict(cave)}
