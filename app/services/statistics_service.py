from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.statistics import Statistics
from app.exceptions import NotFoundError


class StatisticsService:
    @staticmethod
    async def update_statistics(db: AsyncSession, group_id: str, stat_type: str) -> dict:
        result = await db.execute(select(Statistics).where(Statistics.group_id == group_id))
        stat = result.scalar_one_or_none()
        if not stat:
            stat = Statistics(group_id=group_id, data={})
            db.add(stat)
            await db.flush()
        data = stat.data or {}
        data[stat_type] = data.get(stat_type, 0) + 1
        stat.data = data
        await db.flush()
        return {"group_id": group_id, "data": data}
