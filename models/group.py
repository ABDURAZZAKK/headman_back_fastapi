from pydantic import BaseModel
from datetime import datetime


class Group(BaseModel):
    id: int
    name: str
    creater: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class GroupIn(BaseModel):
    name: str