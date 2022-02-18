import datetime
from typing import Optional

from pydantic import BaseModel

from dispatch_data.enum_data import ReplyConfirmStatus


class DispatchConfirmBase(BaseModel):
    dispatch_task_id: int
    provider_name: str
    status: ReplyConfirmStatus
    description: str


class DispatchConfirm(DispatchConfirmBase):
    id: int
    create_time: datetime.datetime

    class Config:
        orm_mode = True


class DispatchConfirmCreate(DispatchConfirmBase):
    pass


class DispatchConfirmUpdate(DispatchConfirmBase):
    dispatch_task_id: Optional[int] = None
    provider_name: Optional[str] = None
    status: Optional[ReplyConfirmStatus] = None
