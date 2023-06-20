import pytest
from httpx import AsyncClient
from repositories import UserRepository
from core.security import verify_password


@pytest.mark.parametrize(
    "id, name, email, password, password2,",
    [
        (1, "Aфыфыв ыфвфвфывbu1", "r1@t.ru", "Qwerty123", "Qwerty123"),
        (2, "Abu2", "root2@root.ru", "Qwerty123", "Qwerty123"),
        (3, "Abu3", "root4@root.ru", "Qwerty123", "Qwerty123"),
        (4, "Abu4", "root5@root.ru", "Qwerty123", "Qwerty123"),
    ],
)
@pytest.mark.asyncio
async def test_get_user(
    ac: AsyncClient,
    userRepo: UserRepository,
    id,
    name,
    email,
    password,
    password2,
):
    ud = {
        "name": name,
        "email": email,
        "password": password,
        "password2": password2,
    }

    await userRepo.create(ud)
    r = await ac.post("/auth/login", json={"email": email, "password": password})
    response = await ac.get(
        f"/users/?u_id={id}",
        headers={
            "Authorization": f'{r.json()["token_type"]} {r.json()["access_token"]}',
        },
    )
    responseAll = await ac.get(f"/users/all")
    assert response.status_code == responseAll.status_code == 200
    user = response.json()
    users = responseAll.json()
    assert len(users) == user["id"]
    assert users[user["id"] - 1] == user
    assert user["id"] == id
    assert user["name"] == ud["name"]
    assert user["email"] == ud["email"]
    assert ud["password"] == ud["password2"]
    assert verify_password(ud["password"], user["hashed_password"])
