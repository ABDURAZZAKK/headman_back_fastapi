import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from tests.conftest import async_session_maker


from repositories import UserRepository
from models import User
from db.models import users


@pytest_asyncio.fixture()
async def userRepo() -> AsyncGenerator[UserRepository, None]:
    async with async_session_maker() as session:
        userRepo = UserRepository(session, users, User)
        yield userRepo
