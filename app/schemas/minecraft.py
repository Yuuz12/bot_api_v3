from typing import Literal
from pydantic import BaseModel


class MCBlacklistCreate(BaseModel):
    qq: str
    email: str | None = None
    online_id: str | None = None
    normal_id: str | None = None
    reason: str | None = None


class MCBlacklistDelete(BaseModel):
    type: Literal[1, 2]
    qq: str | None = None
    id: int | None = None


class MCPingRequest(BaseModel):
    ip: str
    port: int = 25565
