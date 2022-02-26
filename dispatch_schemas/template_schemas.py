import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DispatchTemplateBase(BaseModel):
    dependence: str
    category: str
    level_id: int
    job: str
    location: str
    assign_account_role: Optional[list] = list()
    assign_account_group: Optional[list] = list()
    people_limit: int
    time_limit: datetime.timedelta
    ack_method_id: int


class DispatchTemplate(DispatchTemplateBase):
    id: int
    modify_time: datetime.datetime

    class Config:
        orm_mode = True


class DispatchTemplateCreate(DispatchTemplateBase):
    level_id: Optional[int] = 1
    people_limit: Optional[int] = Field(1, ge=1)
    ack_method_id: Optional[int] = 1


class DispatchTemplateUpdate(DispatchTemplateBase):
    dependence: Optional[str] = None
    category: Optional[str] = None
    level_id: Optional[int] = None
    job: Optional[str] = None
    location: Optional[str] = None
    assign_account_role: Optional[list] = None
    assign_account_group: Optional[list] = None
    people_limit: Optional[int] = None
    time_limit: Optional[datetime.timedelta] = None
    ack_method_id: Optional[int] = None


class DispatchTemplateMultipleUpdate(DispatchTemplateUpdate):
    id: int
