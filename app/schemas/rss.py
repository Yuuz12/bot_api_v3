from pydantic import BaseModel, Field


class RSSSubCreate(BaseModel):
    rss_url: str
    name: str = Field(min_length=1, max_length=100)
    sub_group: str


class RSSSubDelete(BaseModel):
    uid: str
    sub_group: str


class RSSSubUpdate(BaseModel):
    uid: str
    live_status: int | None = None
    dynamic_upload_time: str | None = None
    uname: str | None = None
    roomid: int | None = None


class BilibiliSubCreate(BaseModel):
    uid: str
    sub_group: str
    uname: str | None = None
    roomid: int | None = None


class BilibiliSubDelete(BaseModel):
    uid: str
    sub_group: str


class BilibiliSubUpdate(BaseModel):
    uid: str
    live_status: int | None = None
    dynamic_upload_time: str | None = None
    uname: str | None = None
    roomid: int | None = None
