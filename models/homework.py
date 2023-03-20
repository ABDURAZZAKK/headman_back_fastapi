from datetime import datetime
from pydantic import BaseModel, validator
from enum import Enum



class HWStatus(Enum):
    OPEN = "открыто" 
    CLOSE = "закрыто"



class Homework(BaseModel):
    id: int
    task: str
    status: str
    path_to_files: str | None
    category_id : int
    creater: int
    created_at: datetime
    updated_at: datetime

    @validator('status')
    def status_v(cls, v: str) -> str:
        if v.lower() in [i.value for i in HWStatus]:
            return v.title()
        raise ValueError('Invalid status. It should be "Закрыто" or "Открыто"')



class HomeworkIn(BaseModel):
    task: str
    status: str
    category_id:int
    

    @validator('status')
    def status_v(cls, v: str) -> str:
        if v.lower() in [i.value for i in HWStatus]:
            return v.title()
        raise ValueError('Invalid status. It should be "Закрыто" or "Открыто"')


class HomeworkUpdate(BaseModel):
    task: str|None
    status: str|None
    category_id:int|None
    

    @validator('status')
    def status_v(cls, v: str, values) -> str:
        if not 'status' is None and v.lower() in [i.value for i in HWStatus]:
            return v.title()
        raise ValueError('Invalid status. It should be "Закрыто" or "Открыто"')
