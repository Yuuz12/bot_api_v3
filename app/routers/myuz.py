from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.dependencies import get_db_myuz, verify_token
from app.schemas.common import ResponseBase

router = APIRouter()

@router.get("/info")
async def get_myuz_info(key: str = Depends(verify_token), db: AsyncSession = Depends(get_db_myuz)):
    user_result = await db.execute(text("SELECT COUNT(*) as count FROM cdusers"))
    file_result = await db.execute(text("SELECT COUNT(*) as count FROM cdfiles"))
    user_count = user_result.fetchone()[0]
    file_count = file_result.fetchone()[0]
    return ResponseBase(data={"user_count": user_count, "file_count": file_count})

@router.get("/share-info")
async def get_share_info(created_at: str = Query(...), key: str = Depends(verify_token), db: AsyncSession = Depends(get_db_myuz)):
    created_at_clean = created_at.replace("_", " ")
    result = await db.execute(text("SELECT views, downloads FROM cdshares WHERE created_at = :created_at"), {"created_at": created_at_clean})
    row = result.fetchone()
    if not row:
        return ResponseBase(data={"views": 0, "downloads": 0})
    return ResponseBase(data={"views": row[0], "downloads": row[1]})
