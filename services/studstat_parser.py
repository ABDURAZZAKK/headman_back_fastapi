import httpx
from bs4 import BeautifulSoup
from models import StudstatAcc
from repositories import StudstatAccRepository
from models import StudstatAcc

url = "https://studstat.dgu.ru"


async def auth(data: StudstatAcc) -> httpx.AsyncClient:
    session = httpx.AsyncClient(follow_redirects=True)
    resp = await session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    request_data = {
        "Input.lastname": data.lastname,
        "Input.firstname": data.firstname,
        "Input.patr": data.patr,
        "Input.nbook": data.nbook,
        "__RequestVerificationToken": soup.find(
            "input", attrs={"name": "__RequestVerificationToken"}
        )["value"],
    }

    await session.post(f"{url}/Account/Login?ReturnUrl=%2F", data=request_data)

    return session


async def _get_data(user_id: int, studstatRepo: StudstatAccRepository) -> StudstatAcc:
    return await studstatRepo.get_by_user_id(user_id)


async def _save_cookies(
    data: StudstatAcc, cookies: httpx.Cookies, studstatRepo: StudstatAccRepository
) -> None:
    print(cookies)
    for name, value in cookies.items():
        if name == ".AspNetCore.Cookies":
            await studstatRepo.update(data.id, {"cookie": value})


async def _get_session(data: StudstatAcc, studstatRepo: StudstatAccRepository):
    if data.cookie:
        session = httpx.AsyncClient(follow_redirects=True)
        session.cookies.set(".AspNetCore.Cookies", data.cookie)
        resp = await session.get(f"{url}/Progress")
        if resp.url == f"{url}/Progress":
            return session
    session = await auth(data)
    session_cookie = session.cookies
    await _save_cookies(data, session_cookie, studstatRepo)
    return await _get_session(data, studstatRepo)


async def _get_point_table_resp(session: httpx.AsyncClient, semester_id=None) -> str:
    resp = await session.get(f"{url}/Progress")
    soup = BeautifulSoup(resp.text, "html.parser")
    if not semester_id:
        semester_id = soup.find("option", attrs={"selected": "selected"})["value"]
    stud_id = (
        str(soup.find_all("script", attrs={"type": "text/javascript"})[3])
        .split("var stud_id = ")[1]
        .split(";")[0]
    )
    return await session.get(
        f"{url}/Partial/Progress?stud_id={stud_id}&sess_id={semester_id}"
    )


async def get_point_table_html(user_id, studstatRepo: StudstatAccRepository) -> str:
    data = await _get_data(user_id, studstatRepo)
    session = await _get_session(data, studstatRepo)
    resp = await _get_point_table_resp(session)
    return resp.text
