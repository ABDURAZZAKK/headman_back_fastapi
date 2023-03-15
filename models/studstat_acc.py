from pydantic import BaseModel
from datetime import datetime


class StudstatAcc(BaseModel):
    id: int
    lastname: str
    firstname: str
    patr: str
    nbook: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class StudstatAccIn(BaseModel):
    lastname: str
    firstname: str
    patr: str
    nbook: int
    user_id: int
