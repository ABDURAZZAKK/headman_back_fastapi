from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

class Group(BaseModel):
    id: int
    name: str
    headman: int
    created_at: datetime
    updated_at: datetime

class GroupIn(BaseModel):
    name: str
    headman: int