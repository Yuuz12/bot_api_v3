from typing import Literal
from pydantic import BaseModel


class EmailSendRequest(BaseModel):
    qq: str
    subject: str
    body: str
    sender: Literal["kirino", "shiruku"] = "kirino"
