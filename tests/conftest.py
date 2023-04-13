from typing import Any
from typing import Generator


import pytest
from sqlalchemy import create_engine, MetaData
from starlette.testclient import TestClient
from databases import Database

from core.config import TEST_DATABASE_URL
from db.models import (
                    groups,
                    users,
                    studstat_accs,
                    categories,
                    homeworks,
                    )

from main import app
from main import database

from repositories import UserRepository, GroupRepository, CategoryRepository, HomeworkRepository
from models import User, Group, Category, Homework

CLEAN_TABLES = [
    users,
    groups, 
    categories, 
    homeworks,
]


test_database = Database(TEST_DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    TEST_DATABASE_URL,
)

metadata.create_all(bind=engine)




@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    metadata.create_all(bind=engine)



@pytest.fixture(scope="function", autouse=True)
async def clean_tables():
    for table_for_cleaning in CLEAN_TABLES:
        await table_for_cleaning.query.delete()



@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[database] = test_database
    with TestClient(app) as client:
        yield client



@pytest.fixture
def get_user_repository(database: Database) -> UserRepository:
    return UserRepository(database, users, User)

@pytest.fixture
def get_group_repository(database: Database) -> GroupRepository:
    return GroupRepository(database, groups, Group)

@pytest.fixture
def get_homework_repository(database: Database) -> HomeworkRepository:
    return HomeworkRepository(database, homeworks, Homework)

@pytest.fixture
def get_category_repository(database: Database) -> CategoryRepository:
    return CategoryRepository(database, categories, Category)

