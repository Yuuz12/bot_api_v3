from pydantic import BaseModel, Field


class PrizeDrawRequest(BaseModel):
    qq: str
    coin: int = Field(gt=0)
    type: int = 1


class PrizeCoinRankRequest(BaseModel):
    quantity: int = Field(default=10, gt=0, le=100)
