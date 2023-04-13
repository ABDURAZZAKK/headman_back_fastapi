from fastapi import  APIRouter
from fastapi.responses import  HTMLResponse
from endpoints.depends import get_category_repository, get_group_repository

from serviсes import studstat_parser



router = APIRouter()



@router.get('/points')
async def get_points():
    return HTMLResponse(studstat_parser.get_point_table_html())


@router.post('/create_acc')
async def create_studstat_acc():
    pass


@router.get('/')
async def test():
    groupRepo = get_group_repository()
    categoryRepo = get_category_repository()

    print(await groupRepo.get_all())
    print(await categoryRepo.get_all())


    return {'ok':'ok'}
