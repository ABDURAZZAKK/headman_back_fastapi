from fastapi import APIRouter, Depends, HTTPException, status
from repositories import StudstatAccRepository
from models import StudstatAccIn, User
from .depends import get_studstat_acc_repository, get_current_user
from services import studstat_parser


router = APIRouter()


@router.get("/points_table")
async def get_points_table(
    studstatRepo: StudstatAccRepository = Depends(get_studstat_acc_repository),
    current_user: User = Depends(get_current_user),
):
    return await studstat_parser.get_point_table_html(current_user.id, studstatRepo)


@router.post("/create_acc")
async def create_studstat_acc(
    data: StudstatAccIn,
    studstatAccRepo: StudstatAccRepository = Depends(get_studstat_acc_repository),
    current_user: User = Depends(get_current_user),
):
    session = await studstat_parser.auth(data)
    resp = await session.get(f"{studstat_parser.url}/Progress")
    if resp.url == f"{studstat_parser.url}/Progress":
        data = data.dict() + {"user_id": current_user.id}
        return await studstatAccRepo.create(data)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid data or studstat is not responding",
    )
