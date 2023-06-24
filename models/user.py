from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, constr, root_validator
from .studstat_acc import StudstatAcc


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: constr(min_length=8)

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("password don't match")
        return v


class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    password: constr(min_length=8) | None
    password2: constr(min_length=8) | None

    class Config:
        orm_mode = True

    @root_validator
    def password_match(cls, values):
        pw1, pw2 = values.get("password"), values.get("password2")
        if pw1 != pw2:
            raise ValueError("passwords do not match")
        return values
