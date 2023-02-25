from fastapi import APIRouter, Depends, HTTPException, status
from repositories.groupRepo import GroupRepository
from .depends import get_current_user, get_group_repository
from models.user import User
from models.group import Group, GroupIn


router = APIRouter()


@router.get("/all", response_model=list[Group])
async def get_groups(
        groupRepo: GroupRepository = Depends(get_group_repository),
        limit: int = 100,
        skip: int = 0):

    return await groupRepo.get_all(limit=limit, skip=skip)


@router.get("/{group_id}", response_model=Group)
async def get_group(
        group_id: int,
        groupRepo: GroupRepository = Depends(get_group_repository)):
    
    return await groupRepo.get_by_id(group_id)


@router.post("/", response_model=Group)
async def create_group(
        data: GroupIn,
        groupRepo: GroupRepository = Depends(get_group_repository),
        current_user: User = Depends(get_current_user)):
    
    if current_user and data.headman == current_user.id:
        return await groupRepo.create(d=data)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    


@router.patch("/", response_model=Group)
async def update_user(
        group_id: int,
        data: GroupIn,
        groupRepo: GroupRepository = Depends(get_group_repository),
        current_user: User = Depends(get_current_user)):

    group = await groupRepo.get_by_id(group_id)
    if current_user and group: 
        if data.headman == current_user.id:
            return await groupRepo.update(id=group_id, d=data)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found group")
    


@router.delete("/")
async def delete_user(
        group_id: int,
        groupRepo: GroupRepository = Depends(get_group_repository),
        current_user: User = Depends(get_current_user)):
    
    group = await groupRepo.get_by_id(group_id)
    if current_user and group and group.headman == current_user.id:
        return await groupRepo.delete(id=group_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found group")
    
