from pydantic import BaseModel
from datetime import datetime



class Category(BaseModel):
    id: int
    name: str
    group_id: int
    created_at: datetime
    updated_at: datetime

class CategoryIn(BaseModel):
    name: str
    group_id: int


 
