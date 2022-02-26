from typing import Optional

from pydantic import BaseModel

from dispatch_data.enum_data import ReplyFileType


class DispatchReplyFileBase(BaseModel):
    dispatch_reply_id: int
    filename: str
    file_type: ReplyFileType
    content_type: str
    path: str


class DispatchReplyFileCreate(DispatchReplyFileBase):
    pass


class DispatchReplyFile(DispatchReplyFileBase):
    id: int


class DispatchReplyFileUpdate(DispatchReplyFileBase):
    dispatch_reply_id: Optional[int] = None
    filename: Optional[str] = None
    file_type: Optional[ReplyFileType] = None
    content_type: Optional[str] = None
    path: Optional[str] = None


class DispatchReplyFileMultipleUpdate(DispatchReplyFileUpdate):
    id: int
