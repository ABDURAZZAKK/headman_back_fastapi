from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from repositories.userRepo import UserRepository
from repositories.groupRepo import GroupRepository
from repositories.homeworkRepo import HomeworkRepository
from repositories.categoryRepo import CategoryRepository
from db.base import database
from models.user import User

from db.models import *
from models.user import User
from models.group import Group
from models.category import Category
from models.homework import Homework



def get_user_repository() -> UserRepository:
    return UserRepository(database, users, User)

def get_group_repository() -> GroupRepository:
    return GroupRepository(database, groups, Group)

def get_homework_repository() -> HomeworkRepository:
    return HomeworkRepository(database, homeworks, Homework)

def get_category_repository() -> CategoryRepository:
    return CategoryRepository(database, categories, Category)

async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer())
    ) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get('sub')
    if email is None: 
        raise cred_exception

    user = await users.get_by_email(email=email)
    if user is None: 
        return cred_exception
    return user