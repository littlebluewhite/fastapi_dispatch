import datetime
from typing import Optional

from pydantic import BaseModel

from dispatch_data.enum_data import ReplyConfirmStatus
from dispatch_schemas import reply_file_schemas


class DispatchReplyBase(BaseModel):
    dispatch_task_id: int
    worker_name: str
    status: ReplyConfirmStatus
    description: Optional[str] = None


class DispatchReply(DispatchReplyBase):
    id: int
    create_time: datetime.datetime

    file: list[reply_file_schemas.DispatchReplyFile]

    class Config:
        orm_mode = True


class DispatchReplyCreate(DispatchReplyBase):
    pass


class DispatchReplyUpdate(DispatchReplyBase):
    dispatch_task_id: Optional[int] = None
    worker_name: Optional[str] = None
    status: Optional[ReplyConfirmStatus] = None


class DispatchReplyMultipleUpdate(DispatchReplyUpdate):
    id: int
