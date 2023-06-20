from pydantic import BaseModel
from datetime import datetime



class Category(BaseModel):
    id: int
    name: str
    group_id: int
    creater: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryIn(BaseModel):
    name: str
    group_id: int


class CategoryUpdate(BaseModel):
    name: str | None
    group_id: int | None

 
