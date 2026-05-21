from pydantic import BaseModel


class CaveCreate(BaseModel):
    type: int
    qq: str
    string: str | None = None
    image: str | None = None


class CaveUpdate(BaseModel):
    id: int
    qq: str
    type: int | None = None
    string: str | None = None
    image: str | None = None


class CaveSearch(BaseModel):
    keywords: str
