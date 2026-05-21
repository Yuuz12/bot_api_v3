from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.prize import Prize, PrizeUser
from app.models.user import User
from app.exceptions import NotFoundError, BadRequestError

class PrizeService:
    @staticmethod
    async def get_prize_coin(db: AsyncSession) -> dict:
        result = await db.execute(select(Prize))
        prize = result.scalars().first()
        if not prize:
            return {"coin": 0}
        return {"coin": prize.coin}

    @staticmethod
    async def get_prize_coin_rank(db: AsyncSession, quantity: int) -> list:
        result = await db.execute(
            select(PrizeUser).order_by(PrizeUser.coin.desc()).limit(quantity)
        )
        users = result.scalars().all()
        return [{"qq": u.qq, "coin": u.coin} for u in users]

    @staticmethod
    async def draw_prize(db: AsyncSession, qq: str, coin: int, draw_type: int) -> dict:
        result = await db.execute(select(User).where(User.qq == qq))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("用户不存在")
        if user.coin < coin:
            raise BadRequestError("金币不足")

        user.coin -= coin

        result = await db.execute(select(Prize))
        prize = result.scalars().first()
        if not prize:
            prize = Prize(coin=0)
            db.add(prize)
            await db.flush()
        prize.coin += coin

        result = await db.execute(select(PrizeUser).where(PrizeUser.qq == qq))
        prize_user = result.scalar_one_or_none()
        if not prize_user:
            prize_user = PrizeUser(qq=qq, coin=0)
            db.add(prize_user)
            await db.flush()
        prize_user.coin += coin

        import random
        win = random.random() < 0.01
        win_amount = 0
        if win and prize.coin > 0:
            win_amount = min(prize.coin, int(prize.coin * 0.5))
            user.coin += win_amount
            prize.coin -= win_amount

        await db.flush()
        return {
            "qq": user.qq,
            "coin_spent": coin,
            "won": win,
            "win_amount": win_amount,
            "current_coin": user.coin,
            "prize_pool": prize.coin,
        }
