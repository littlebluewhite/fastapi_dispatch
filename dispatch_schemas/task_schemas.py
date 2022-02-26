import datetime
from typing import Optional

from pydantic import BaseModel, Field

from dispatch_schemas.confirm_schemas import DispatchConfirm
from dispatch_schemas.reply_schemas import DispatchReply


class DispatchTaskBase(BaseModel):
    bind_event_id: Optional[str] = None
    category: Optional[str] = None
    level_id: int
    provider: str
    job: str
    location: str
    assign_account: Optional[list[str]] = list()
    assign_account_role: Optional[list[str]] = list()
    assign_account_group: Optional[list[str]] = list()
    people_limit: int
    order_taker: Optional[list[str]] = list()
    deadline: datetime.datetime
    ack_method_id: int
    status_id: int


class DispatchTask(DispatchTaskBase):
    id: int
    dispatch_event_id: str
    isActive: bool
    start_time: datetime.datetime
    update_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None

    reply: list[DispatchReply]
    confirm: list[DispatchConfirm]

    class Config:
        orm_mode = True


class DispatchTaskCreate(DispatchTaskBase):
    level_id: Optional[int] = 1
    people_limit: Optional[int] = Field(1, ge=1)
    ack_method_id: Optional[int] = 1
    status_id: Optional[int] = 1


class DispatchTaskUpdate(DispatchTaskBase):
    level_id: Optional[int] = None
    provider: Optional[str] = None
    job: Optional[str] = None
    location: Optional[str] = None
    people_limit: Optional[int] = None
    assign_account: Optional[list[str]] = None
    assign_account_role: Optional[list[str]] = None
    assign_account_group: Optional[list[str]] = None
    order_taker: Optional[list[str]] = None
    isActive: Optional[bool] = None
    deadline: Optional[datetime.datetime] = None
    ack_method_id: Optional[int] = None
    status_id: Optional[int] = None
    end_time: Optional[datetime.datetime] = None


class DispatchTaskWrite(DispatchTaskCreate):
    dispatch_event_id: str


class DispatchTaskMultipleUpdate(DispatchTaskUpdate):
    id: int
