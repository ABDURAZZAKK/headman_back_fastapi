from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import get_async_session
from db.models import *

from repositories import (
    UserRepository,
    GroupRepository,
    CategoryRepository,
    HomeworkRepository,
)
from models import User, Group, Category, Homework


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session, users, User)


async def get_group_repository() -> GroupRepository:
    return GroupRepository(await get_async_session(), groups, Group)


async def get_homework_repository() -> HomeworkRepository:
    return HomeworkRepository(await get_async_session(), homeworks, Homework)


async def get_category_repository() -> CategoryRepository:
    return CategoryRepository(await get_async_session(), categories, Category)


async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid"
    )
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception

    user = await users.get_by_email(email=email)
    if user is None:
        return cred_exception
    return user
