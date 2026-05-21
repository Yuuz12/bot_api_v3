from pydantic import BaseModel


class StatisticsUpdate(BaseModel):
    group_id: str
    stat_type: str
