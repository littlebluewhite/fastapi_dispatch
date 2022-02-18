from typing import Optional

from pydantic import BaseModel


class DispatchStatusBase(BaseModel):
    name: str
    description: str


class DispatchStatus(DispatchStatusBase):
    id: int

    class Config:
        orm_mode = True


class DispatchStatusCreate(DispatchStatusBase):
    pass


class DispatchStatusUpdate(DispatchStatusBase):
    name: Optional[str] = None
    description: Optional[str] = None
