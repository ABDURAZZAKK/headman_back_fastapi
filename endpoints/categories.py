from fastapi import APIRouter, Depends, HTTPException, status
from repositories.categoryRepo import CategoryRepository
from .depends import get_current_user, get_category_repository, get_group_repository
from models.user import User
from models.category import Category, CategoryIn


router = APIRouter()


@router.get("/all", response_model=list[Category])
async def get_categories(
        limit: int = 100,
        skip: int = 0,
        categorypRepo: CategoryRepository = Depends(get_category_repository)
        ):
    return await categorypRepo.get_all(limit=limit, skip=skip)


@router.get("/group/{group_id}", response_model=list[Category])
async def get_category_by_group_id(
        group_id: int,
        limit: int = 100,
        skip: int = 0,
        categorypRepo: CategoryRepository = Depends(get_category_repository),
        ):
    return await categorypRepo.get_by_group_id(group_id, limit, skip)


@router.post("/", response_model=Category)
async def create_category(
        data: CategoryIn,
        categorypRepo: CategoryRepository = Depends(get_category_repository),
        current_user: User = Depends(get_current_user)
        ):

    groupRepo = get_group_repository()
    group = await groupRepo.get_by_id(data.group_id)
    if group:
        if current_user and group.headman == current_user.id:
            return await categorypRepo.create(d=data)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found group")
    

@router.patch("/", response_model=Category)
async def update_category(
        categoty_id: int,
        data: CategoryIn,
        categorypRepo: CategoryRepository = Depends(get_category_repository),
        current_user: User = Depends(get_current_user)):

    category = await categorypRepo.get_by_id(categoty_id)
    if current_user and category:
        groupRepo = get_group_repository()
        group = await groupRepo.get_by_id(data.group_id)
        if group and group.headman == current_user.id:
            return await categorypRepo.update(id=categoty_id, d=data)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found category")
    

@router.delete("/")
async def delete_category(
        categoty_id: int,
        categorypRepo: CategoryRepository = Depends(get_category_repository),
        current_user: User = Depends(get_current_user)):
    
    category = await categorypRepo.get_by_id(categoty_id)
    if current_user and category:
        groupRepo = get_group_repository()
        group = await groupRepo.get_by_id(category.group_id)
        if group and group.headman == current_user.id:
            return await categorypRepo.delete(id=categoty_id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found category")