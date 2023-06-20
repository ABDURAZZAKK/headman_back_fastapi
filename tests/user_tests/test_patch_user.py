import pytest
from httpx import AsyncClient
from repositories import UserRepository
from models import User
from core.security import verify_password


@pytest.mark.parametrize(
    "id, data, was, became,status_code",
    [
        # Валидные данные
        (
            1,
            {"name": "TestDone"},
            {"name": "Abu1", "email": "root1@root.ru", "password": "Qwerty123"},
            {"name": "TestDone", "email": "root1@root.ru", "password": "Qwerty123"},
            200,
        ),
        # Валидные данные мультиданные
        (
            2,
            {
                "name": "TestDone",
                "email": "TestDone@root.ru",
                "password": "TestDone1234",
                "password2": "TestDone1234",
            },
            {"name": "Abu2", "email": "root2@root.ru", "password": "Qwerty123"},
            {
                "name": "TestDone",
                "email": "TestDone@root.ru",
                "password": "TestDone1234",
            },
            200,
        ),
        # already email
        (
            3,
            {
                "email": "root1@root.ru",
            },
            {"name": "Abu3", "email": "root3@root.ru", "password": "Qwerty123"},
            {"name": "Abu3", "email": "root3@root.ru", "password": "Qwerty123"},
            409,
        ),
        # нет одного из паролей
        (
            4,
            {
                "password": "TestDone1234",
            },
            {"name": "Abu4", "email": "root4@root.ru", "password": "Qwerty123"},
            {
                "name": "Abu4",
                "email": "root4@root.ru",
                "password": "Qwerty123",
            },
            422,
        ),
        # пароли не равны
        (
            5,
            {
                "password": "TestDone1234",
                "password2": "TetDone1234",
            },
            {"name": "Abu5", "email": "root5@root.ru", "password": "Qwerty123"},
            {
                "name": "Abu5",
                "email": "root5@root.ru",
                "password": "Qwerty123",
            },
            422,
        ),
    ],
)
@pytest.mark.asyncio
async def test_patch_user(
    ac: AsyncClient,
    userRepo: UserRepository,
    id,
    data,
    was,
    became,
    status_code,
):
    ud = {
        "name": was["name"],
        "email": was["email"],
        "password": was["password"],
        "password2": was["password"],
    }

    await userRepo.create(ud)
    r = await ac.post(
        "/auth/login", json={"email": was["email"], "password": was["password"]}
    )

    header = {"Authorization": f'{r.json()["token_type"]} {r.json()["access_token"]}'}

    r = await ac.patch(f"/users/?u_id={id}", headers=header, json=data)

    assert r.status_code == status_code
    u = User.from_orm(await userRepo.get_by_id(id))
    print("\n", u)
    assert u.id == id
    assert u.name == became["name"]
    assert u.email == became["email"]
    assert verify_password(became["password"], u.hashed_password)

    if r.status_code == 200:
        assert r.json()["status"] == "success"
