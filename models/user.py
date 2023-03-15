from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: int 
    name: str
    email: EmailStr
    hashed_password: str
    studstat_acc_id: int|None
    created_at: datetime
    updated_at: datetime

class UserIn(BaseModel):
    name: str
    email: EmailStr
    studstat_acc_id: int|None
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("password don't match")
        return v

class UserOut(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime