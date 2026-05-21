from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, verify_token
from app.schemas.common import ResponseBase
from app.schemas.user import (
    UserCheckRequest,
    UserCoinSet,
    UserCoinUpdate,
    UserCreate,
    UserFavorabilitySet,
    UserFavorabilityUpdate,
    UserItemBuy,
    UserItemUse,
    UserUpdateFstEmail,
    UserUpdateGroup,
    UserUpdateKookId,
    UserUpdateName,
    UserUpdateOsuMode,
    UserUpdateOsuName,
    UserUpdateQQGuildId,
    UserUpdateTelegramName,
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=ResponseBase)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.create_user(db, body.qq, body.group)
    return ResponseBase(data=data)


@router.get("/info", response_model=ResponseBase)
async def get_user_info(
    qq: str | None = Query(None),
    kook_id: str | None = Query(None),
    telegram_name: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    if qq:
        data = await UserService.get_user_by_qq(db, qq)
    elif kook_id:
        data = await UserService.get_user_by_kook_id(db, kook_id)
    elif telegram_name:
        data = await UserService.get_user_by_telegram_name(db, telegram_name)
    else:
        return ResponseBase(code=400, message="请提供 qq、kook_id 或 telegram_name 其中一个参数")
    return ResponseBase(data=data)


@router.post("/check", response_model=ResponseBase)
async def check_in(
    body: UserCheckRequest,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.check_in(db, body.qq, body.type, body.value)
    return ResponseBase(data=data)


@router.put("/name", response_model=ResponseBase)
async def update_name(
    body: UserUpdateName,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_name(db, body.qq, body.name)
    return ResponseBase(data=data)


@router.put("/osu-name", response_model=ResponseBase)
async def update_osu_name(
    body: UserUpdateOsuName,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_osu_name(db, body.qq, body.osu_name)
    return ResponseBase(data=data)


@router.put("/osu-mode", response_model=ResponseBase)
async def update_osu_mode(
    body: UserUpdateOsuMode,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_osu_mode(db, body.qq, body.osu_mode)
    return ResponseBase(data=data)


@router.put("/kook-id", response_model=ResponseBase)
async def update_kook_id(
    body: UserUpdateKookId,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_kook_id(db, body.qq, body.kook_id)
    return ResponseBase(data=data)


@router.put("/qqguild-id", response_model=ResponseBase)
async def update_qqguild_id(
    body: UserUpdateQQGuildId,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_qqguild_id(db, body.qq, body.qqguild_id)
    return ResponseBase(data=data)


@router.put("/telegram-name", response_model=ResponseBase)
async def update_telegram_name(
    body: UserUpdateTelegramName,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_telegram_name(db, body.qq, body.telegram_name)
    return ResponseBase(data=data)


@router.put("/fst-email", response_model=ResponseBase)
async def update_fst_email(
    body: UserUpdateFstEmail,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_fst_email(db, body.qq, body.fst_email)
    return ResponseBase(data=data)


@router.put("/group", response_model=ResponseBase)
async def update_group(
    body: UserUpdateGroup,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_group(db, body.qq, body.group)
    return ResponseBase(data=data)


@router.patch("/favorability", response_model=ResponseBase)
async def update_favorability(
    body: UserFavorabilityUpdate,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_favorability(db, body.qq, body.type, body.value)
    return ResponseBase(data=data)


@router.patch("/coin", response_model=ResponseBase)
async def update_coin(
    body: UserCoinUpdate,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.update_coin(db, body.qq, body.type, body.value)
    return ResponseBase(data=data)


@router.put("/favorability/set", response_model=ResponseBase)
async def set_favorability(
    body: UserFavorabilitySet,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.set_favorability(db, body.qq, body.value)
    return ResponseBase(data=data)


@router.put("/coin/set", response_model=ResponseBase)
async def set_coin(
    body: UserCoinSet,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.set_coin(db, body.qq, body.value)
    return ResponseBase(data=data)


@router.post("/item/use", response_model=ResponseBase)
async def use_item(
    body: UserItemUse,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.use_item(db, body.qq, body.item_name)
    return ResponseBase(data=data)


@router.post("/item/buy", response_model=ResponseBase)
async def buy_item(
    body: UserItemBuy,
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.buy_item(db, body.qq, body.item_name, body.quantity)
    return ResponseBase(data=data)


@router.get("/coin/all", response_model=ResponseBase)
async def get_all_coin(
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.get_all_coin(db)
    return ResponseBase(data=data)


@router.get("/check-rank", response_model=ResponseBase)
async def get_check_rank(
    date: str = Query(...),
    quantity: int = Query(default=10, gt=0, le=100),
    db: AsyncSession = Depends(get_db),
    _token: str = Depends(verify_token),
):
    data = await UserService.get_check_rank(db, date, quantity)
    return ResponseBase(data=data)
