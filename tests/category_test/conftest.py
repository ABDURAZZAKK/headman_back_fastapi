import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from tests.conftest import async_session_maker


from repositories import CategoryRepository
from models import Category
from db.models import categories


@pytest_asyncio.fixture()
async def categoryRepo() -> AsyncGenerator[CategoryRepository, None]:
    async with async_session_maker() as session:
        userRepo = CategoryRepository(session, categories, Category)
        yield userRepo
