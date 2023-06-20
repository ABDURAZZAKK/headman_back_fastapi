import pytest
from httpx import AsyncClient
from repositories import UserRepository


@pytest.mark.parametrize(
    "id, name, email, password1, password2, verify_password, auth_status_code, status_code",
    [
        # Валидные данные
        (1, "Abu1", "root1@root.ru", "Qwerty123", "Qwerty123", "Qwerty123", 200, 200),
        # ID не найден
        # Так как база 1 на все тесты, и ID автоикремент, второй раз не может быть ID=1
        (1, "Abu1", "root1@root.ru", "Qwerty123", "Qwerty123", "Qwerty123", 200, 404),
        # Проверка на то что ничего не сломалось после предыдущих тестов
        (3, "Abu1", "root1@root.ru", "Qwerty123", "Qwerty123", "Qwerty123", 200, 200),
        # Ивалидный пароль, auth_status_code - 401 Unauthorized
        (4, "Abu1", "root1@root.ru", "Qwerty123", "Qwerty123", "123", 0, 403),
    ],
)
@pytest.mark.asyncio
async def test_delete_user(
    ac: AsyncClient,
    userRepo: UserRepository,
    id,
    name,
    email,
    password1,
    password2,
    verify_password,
    status_code,
    auth_status_code,
):
    ud = {
        "name": name,
        "email": email,
        "password": password1,
        "password2": password2,
    }
    header = {}

    await userRepo.create(ud)
    r = await ac.post("/auth/login", json={"email": email, "password": verify_password})
    if r.status_code == auth_status_code:
        header = {
            "Authorization": f'{r.json()["token_type"]} {r.json()["access_token"]}',
        }

    r = await ac.delete(
        f"/users/?u_id={id}",
        headers=header,
    )

    assert r.status_code == status_code
    if r.status_code == 200:
        assert r.json()["status"] == "success"

        assert len(await userRepo.get_all()) == 0
        assert await userRepo.get_by_email(email) is None

    else:
        u = await userRepo.get_by_email(email)
        await userRepo.delete(u[0])
