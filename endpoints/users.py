from fastapi import APIRouter, Depends, HTTPException, status
from repositories import UserRepository
from .depends import get_current_user, get_user_repository
from models import User, UserIn, UserUpdate
from .utils import dict_without_null_from_pydantic_model
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/all", response_model=list[User])
async def get_users(
    userRepo: UserRepository = Depends(get_user_repository),
    limit: int = 100,
    skip: int = 0,
):
    return await userRepo.get_all(limit=limit, skip=skip)


@router.get("/", response_model=User)
async def get_user(
    u_id: int,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    return await userRepo.get_by_id(id=u_id)


@router.post("/", response_model=User)
async def create_user(
    user: UserIn, userRepo: UserRepository = Depends(get_user_repository)
):
    try:
        return await userRepo.create(d=user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )


@router.patch("/")
async def update_user(
    u_id: int,
    data: UserUpdate,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    user = await userRepo.get_by_id(u_id)
    if user:
        if user.email == current_user.email:
            data = dict_without_null_from_pydantic_model(data)
            try:
                return await userRepo.update(id=u_id, d=data)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")


@router.delete("/")
async def delete_user(
    u_id: int,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    if u_id == current_user.id:
        return await userRepo.delete(id=u_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
