from typing import Optional

from pydantic import BaseModel


class DispatchLevelBase(BaseModel):
    name: str
    description: str
    color_code: list


class DispatchLevel(DispatchLevelBase):
    id: int

    class Config:
        orm_mode = True


class DispatchLevelCreate(DispatchLevelBase):
    pass


class DispatchLevelUpdate(DispatchLevelBase):
    name: Optional[str] = None
    description: Optional[str] = None
    color_code: Optional[list] = None


class DispatchLevelMultipleUpdate(DispatchLevelUpdate):
    id: int
