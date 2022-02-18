from typing import Optional

from pydantic import BaseModel


class DispatchAckMethodBase(BaseModel):
    name: str
    description: str
    need_text: bool
    need_photo: bool
    need_video: bool


class DispatchAckMethod(DispatchAckMethodBase):
    id: int

    class Config:
        orm_mode = True


class DispatchAckMethodCreate(DispatchAckMethodBase):
    pass


class DispatchAckMethodUpdate(DispatchAckMethodBase):
    name: Optional[str] = None
    description: Optional[str] = None
    need_text: Optional[bool] = None
    need_photo: Optional[bool] = None
    need_video: Optional[bool] = None
