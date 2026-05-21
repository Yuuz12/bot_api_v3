from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    qq: str
    group: int | None = None


class UserInfoResponse(BaseModel):
    id: int | None = None
    qq: str | None = None
    name: str | None = None
    kook_id: str | None = None
    telegram_name: str | None = None
    qqguild_id: str | None = None
    osu_name: str | None = None
    osu_mode: str | None = None
    fst_email: str | None = None
    favorability: int | None = None
    coin: int | None = None
    check_in_time_last: str | None = None
    check_number: int | None = None
    check_continuous_number: int | None = None
    check_rank: int | None = None
    status: int | None = None
    user_group: int | None = None
    registered_time: str | None = None
    registered_timestamp: int | None = None
    item: str | None = None
    badge: str | None = None


class UserCheckRequest(BaseModel):
    qq: str
    type: int = 0
    value: int | None = None


class UserUpdateName(BaseModel):
    qq: str
    name: str = Field(min_length=3, max_length=16)


class UserUpdateOsuName(BaseModel):
    qq: str
    osu_name: str = Field(min_length=3, max_length=15)


class UserUpdateOsuMode(BaseModel):
    qq: str
    osu_mode: Literal["osu", "mania", "taiko", "ctb"]


class UserUpdateKookId(BaseModel):
    qq: str
    kook_id: str


class UserUpdateQQGuildId(BaseModel):
    qq: str
    qqguild_id: str


class UserUpdateTelegramName(BaseModel):
    qq: str
    telegram_name: str


class UserUpdateFstEmail(BaseModel):
    qq: str
    fst_email: EmailStr


class UserUpdateGroup(BaseModel):
    qq: str
    group: int


class UserFavorabilityUpdate(BaseModel):
    qq: str
    type: Literal[1, 2]
    value: int = Field(gt=0)


class UserCoinUpdate(BaseModel):
    qq: str
    type: Literal[1, 2]
    value: int = Field(gt=0)


class UserFavorabilitySet(BaseModel):
    qq: str
    value: int


class UserCoinSet(BaseModel):
    qq: str
    value: int


class UserItemUse(BaseModel):
    qq: str
    item_name: str


class UserItemBuy(BaseModel):
    qq: str
    item_name: str
    quantity: int = Field(default=1, gt=0)


class UserCheckRankRequest(BaseModel):
    date: str
    quantity: int = Field(default=10, gt=0, le=100)
