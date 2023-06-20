import json
import pytest
from httpx import AsyncClient
from core.security import verify_password
from repositories import UserRepository
from models import User


@pytest.mark.parametrize(
    "name, email, password, password2, status_code, len_users, validity",
    [
        # Валидные данные
        ("Abu", "root@root.ru", "Qwerty123", "Qwerty123", 200, 1, True),
        # Такой email уже существует
        ("Abu", "root@root.ru", "Qwerty123", "Qwerty123", 409, 1, False),
        # Инвалидный email
        ("Abu", "rootroot.ru", "Qwerty123", "Qwerty123", 422, 1, False),
        # Инвалидный пароль
        ("Abu1", "root1@root.ru", "1", "1", 422, 1, False),
    ],
)
@pytest.mark.asyncio
async def test_register_response(
    ac: AsyncClient,
    userRepo: UserRepository,
    name,
    email,
    password,
    password2,
    status_code,
    len_users,
    validity,
):
    ud = {
        "name": name,
        "email": email,
        "password": password,
        "password2": password2,
    }
    response = await ac.post("/users/", json=ud)
    all_users = await userRepo.get_all()

    assert response.status_code == status_code
    assert len(all_users) == len_users
    if validity:
        for resp in (json.loads(response.content), dict(User.from_orm(all_users[0]))):
            assert resp["name"] == ud["name"]
            assert resp["email"] == ud["email"]
            assert verify_password("Qwerty123", resp["hashed_password"])
