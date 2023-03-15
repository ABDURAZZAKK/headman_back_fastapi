from fastapi import  APIRouter
from fastapi.responses import  HTMLResponse

from serviсes import points_parser



router = APIRouter()



@router.get('/points')
async def get_points():
    return HTMLResponse(points_parser.get_point_table_html())


