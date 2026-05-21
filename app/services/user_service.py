import json
import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestError, NotFoundError
from app.models.item import Item
from app.models.user import User


class UserService:
    @staticmethod
    def _parse_item(item_str: str | None) -> dict:
        if not item_str:
            return {}
        try:
            return json.loads(item_str)
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            return json.loads(item_str.replace("|", "\""))
        except (json.JSONDecodeError, TypeError):
            return {}

    @staticmethod
    def _dump_item(item_dict: dict) -> str:
        return json.dumps(item_dict, ensure_ascii=False)

    @staticmethod
    def _user_to_dict(user: User) -> dict:
        return {
            "id": user.id,
            "qq": user.qq,
            "name": user.name,
            "kook_id": user.kook_id,
            "telegram_name": user.telegram_name,
            "qqguild_id": user.qqguild_id,
            "osu_name": user.osu_name,
            "osu_mode": user.osu_mode,
            "fst_email": user.fst_email,
            "favorability": user.favorability,
            "coin": user.coin,
            "check_in_time_last": user.check_in_time_last,
            "check_number": user.check_number,
            "check_continuous_number": user.check_continuous_number,
            "check_rank": user.check_rank,
            "status": user.status,
            "user_group": user.user_group,
            "registered_time": user.registered_time,
            "registered_timestamp": user.registered_timestamp,
            "item": user.item,
            "badge": user.badge,
        }

    @staticmethod
    async def create_user(db: AsyncSession, qq: str, group: int | None = None) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        existing = result.scalar_one_or_none()
        if existing:
            return UserService._user_to_dict(existing)
        user = User(qq=qq, name="DEFAULT_USER_NAME", user_group=group or 0)
        db.add(user)
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def get_user_by_qq(db: AsyncSession, qq: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")
        return UserService._user_to_dict(user)

    @staticmethod
    async def get_user_by_kook_id(db: AsyncSession, kook_id: str) -> dict:
        result = await db.execute(select(User).where(User.kook_id == kook_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")
        return UserService._user_to_dict(user)

    @staticmethod
    async def get_user_by_telegram_name(db: AsyncSession, telegram_name: str) -> dict:
        result = await db.execute(select(User).where(User.telegram_name == telegram_name))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")
        return UserService._user_to_dict(user)

    @staticmethod
    async def check_in(db: AsyncSession, qq: str, check_type: int = 0, value: int | None = None) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        tz = timezone(timedelta(hours=8))
        now = datetime.now(tz)
        today_str = now.strftime("%Y-%m-%d")
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        if user.check_in_time_last and user.check_in_time_last.startswith(today_str):
            raise BadRequestError("今日已签到")

        if user.check_in_time_last and user.check_in_time_last.startswith(yesterday_str):
            user.check_continuous_number += 1
        else:
            user.check_continuous_number = 1

        user.check_number += 1

        rank_result = await db.execute(
            select(func.count()).select_from(User).where(User.check_in_time_last.like(f"{today_str}%"))
        )
        user.check_rank = (rank_result.scalar() or 0) + 1

        if value is not None:
            reward = value
        else:
            reward = round(5 * math.log(math.e + user.check_continuous_number))

        user.favorability += reward
        user.coin += reward
        user.check_in_time_last = now_str

        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_name(db: AsyncSession, qq: str, name: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        is_first_time = user.name == "DEFAULT_USER_NAME"
        user.name = name

        if is_first_time:
            tz = timezone(timedelta(hours=8))
            now = datetime.now(tz)
            user.registered_time = now.strftime("%Y-%m-%d %H:%M:%S")
            user.registered_timestamp = int(now.timestamp())

        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_osu_name(db: AsyncSession, qq: str, osu_name: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.osu_name = osu_name
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_osu_mode(db: AsyncSession, qq: str, osu_mode: str) -> dict:
        valid_modes = ("osu", "mania", "taiko", "ctb")
        if osu_mode not in valid_modes:
            raise BadRequestError(f"无效的 osu! 模式，可选值: {', '.join(valid_modes)}")

        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.osu_mode = osu_mode
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_kook_id(db: AsyncSession, qq: str, kook_id: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.kook_id = kook_id
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_qqguild_id(db: AsyncSession, qq: str, qqguild_id: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.qqguild_id = qqguild_id
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_telegram_name(db: AsyncSession, qq: str, telegram_name: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.telegram_name = telegram_name
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_fst_email(db: AsyncSession, qq: str, fst_email: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.fst_email = fst_email
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_group(db: AsyncSession, qq: str, group: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.user_group = group
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_favorability(db: AsyncSession, qq: str, type: int, value: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        if type == 1:
            user.favorability += value
        elif type == 2:
            user.favorability = max(0, user.favorability - value)
        else:
            raise BadRequestError("无效的操作类型，1=增加 2=减少")

        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def update_coin(db: AsyncSession, qq: str, type: int, value: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        if type == 1:
            user.coin += value
        elif type == 2:
            user.coin = max(0, user.coin - value)
        else:
            raise BadRequestError("无效的操作类型，1=增加 2=减少")

        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def set_favorability(db: AsyncSession, qq: str, value: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.favorability = value
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def set_coin(db: AsyncSession, qq: str, value: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        user.coin = value
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def use_item(db: AsyncSession, qq: str, item_name: str) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        items = UserService._parse_item(user.item)
        if item_name not in items:
            raise NotFoundError("物品不存在")
        if items[item_name] <= 0:
            raise BadRequestError("物品数量不足")

        items[item_name] -= 1
        if items[item_name] <= 0:
            del items[item_name]

        user.item = UserService._dump_item(items)
        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def buy_item(db: AsyncSession, qq: str, item_name: str, quantity: int = 1) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")

        item_result = await db.execute(select(Item).where(Item.name == item_name))
        item = item_result.scalar_one_or_none()
        if not item:
            raise NotFoundError("商品不存在")

        total_cost_coin = item.cost_coin * quantity
        total_cost_favorability = item.cost_favorability * quantity

        if user.favorability < item.need_favorability:
            raise BadRequestError("好感度未达到购买要求")
        if user.coin < total_cost_coin:
            raise BadRequestError("硬币不足")
        if user.favorability < total_cost_favorability:
            raise BadRequestError("好感度不足")

        user.coin -= total_cost_coin
        user.favorability -= total_cost_favorability

        items = UserService._parse_item(user.item)
        items[item_name] = items.get(item_name, 0) + quantity
        user.item = UserService._dump_item(items)

        await db.flush()
        return UserService._user_to_dict(user)

    @staticmethod
    async def get_all_coin(db: AsyncSession) -> dict:
        result = await db.execute(
            select(func.sum(User.coin)).where(
                User.name != "DEFAULT_USER_NAME",
                User.user_group != 52,
            )
        )
        total_coin = result.scalar() or 0
        return {"total_coin": total_coin}

    @staticmethod
    async def get_check_rank(db: AsyncSession, date: str, quantity: int = 10) -> list[dict]:
        result = await db.execute(
            select(User)
            .where(User.check_in_time_last.like(f"{date}%"))
            .order_by(User.check_rank)
            .limit(quantity)
        )
        users = result.scalars().all()
        return [UserService._user_to_dict(u) for u in users]
