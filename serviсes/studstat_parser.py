import requests
from bs4 import BeautifulSoup
import json



url = 'http://studstat.dgu.ru'
data = {"Input.lastname": "Магомедов",
        "Input.firstname": "Абдуразак",
        "Input.patr": "Абдурахманович",
        "Input.nbook": "11514"}


def auth(data):
    session = requests.Session()
    
    soup = BeautifulSoup(session.get(url).text, "html.parser")

    data["__RequestVerificationToken"] = soup.find('input', attrs={'name':'__RequestVerificationToken'})['value']
    session.post(f"{url}/Account/Login?ReturnUrl=%2F",data=data)

    return session


# def seve_cookies(cookies):
#     cookies_dict = [
#         {"domain": key.domain, "name": key.name, "path":key.path, "value": key.value}
#          for key in cookies
#     ]
#     with open('t.txt', 'w', encoding='utf-8') as f:
#         for i in cookies_dict:
#             f.write(str(i)+'\n')


# def get_cookies():
#     cookies = []
#     try:
#         with open('t.txt', 'r', encoding='utf-8') as f:
#             for i in f.readlines():
#                 cookies.append(json.loads(i.replace("'",'"')))
#     except:
#         cookies = []
#     return cookies


# def get_session():
#     cookies = get_cookies()
#     if cookies:
#         session = requests.Session()
#         for c in cookies:
#             session.cookies.set(**c)
#         if session.get(f'{url}/Progress').url == f'{url}/Progress':
#             return session
    
#     seve_cookies(registration(data).cookies)
#     return get_session()


def get_point_table_resp(session, semester_id=None):
    soup = BeautifulSoup(session.get(f'{url}/Progress').text, "html.parser")
    if not semester_id:
        semester_id = soup.find('option', attrs={"selected":"selected"})['value']
    stud_id = str(soup.find_all('script', attrs={"type":"text/javascript"})[3]).split("var stud_id = ")[1].split(';')[0]
    return session.get(f"{url}/Partial/Progress?stud_id={stud_id}&sess_id={semester_id}")


def get_point_table_html(data):
    session = auth(data)
    return get_point_table_resp(session).text

