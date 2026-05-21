from pydantic import BaseModel


class InvitationObtainRequest(BaseModel):
    qq: str


class InvitationQueryRequest(BaseModel):
    qq: str
