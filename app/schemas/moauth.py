from pydantic import BaseModel


class MOAuthCreate(BaseModel):
    qq: str
    kook_id: str
    name: str


class MOAuthBindKook(BaseModel):
    qq: str
    key: str
