from fastapi import APIRouter, Depends, HTTPException, status
from repositories.userRepo import UserRepository
from .depends import get_current_user, get_user_repository
from models.user import User, UserIn, UserUpdate
from .utils import delete_none_from_pydantic_model


router = APIRouter()

@router.get("/all", response_model=list[User])
async def get_users(
    userRepo: UserRepository = Depends(get_user_repository),
    limit: int = 100,
    skip: int = 0):

    return await userRepo.get_all(limit=limit, skip=skip)


@router.get("/{u_id}", response_model=User)
async def update_user(
    u_id: int,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)):

    return await userRepo.get_by_id(id=u_id)
    
@router.post("/", response_model=User)
async def create_user(
    user: UserIn,
    userRepo: UserRepository = Depends(get_user_repository)):

    return await userRepo.create(d=user)
    

@router.patch("/", response_model=User)
async def update_user(
    u_id: int,
    data: UserUpdate,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)):

    user = await userRepo.get_by_id(u_id)
    if user: 
        if user.email == current_user.email:
            data = delete_none_from_pydantic_model(data)
            return await userRepo.update(id=u_id, d=data)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    


@router.delete("/")
async def delete_user(
    u_id: int,
    userRepo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)):

    if u_id == current_user.id:
        return await userRepo.delete(id=u_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    
    