from pydantic import BaseModel
from datetime import datetime


class StudstatAcc(BaseModel):
    id: int
    lastname: str
    firstname: str
    patr: str
    nbook: int
    user_id: int
    cookie: str | None
    created_at: datetime
    updated_at: datetime


class StudstatAccIn(BaseModel):
    lastname: str
    firstname: str
    patr: str
    nbook: int
    user_id: int|None


class StudstatAccUpdate(BaseModel):
    lastname: str | None
    firstname: str | None
    patr: str | None
    nbook: int | None
    cookie: str | None
