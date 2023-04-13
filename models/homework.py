from datetime import datetime
from pydantic import BaseModel, validator
from enum import Enum



class HWStatus(str, Enum):
    OPEN = "открыто" 
    CLOSE = "закрыто"



class Homework(BaseModel):
    id: int
    task: str
    status: HWStatus
    path_to_files: str | None
    category_id : int
    creater: int
    created_at: datetime
    updated_at: datetime


class HomeworkIn(BaseModel):
    task: str
    status: HWStatus
    category_id:int


class HomeworkUpdate(BaseModel):
    task: str|None
    status: HWStatus|None
    category_id:int|None
