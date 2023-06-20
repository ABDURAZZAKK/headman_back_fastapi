from fastapi import APIRouter, Depends, HTTPException, status
from repositories import CategoryRepository
from .depends import get_current_user, get_category_repository, get_group_repository
from .utils import add_creater_field_to_dict, dict_without_null_from_pydantic_model
from models import User, Category, CategoryIn, CategoryUpdate


router = APIRouter()


@router.get("/all", response_model=list[Category])
async def get_categories(
    limit: int = 100,
    skip: int = 0,
    categorypRepo: CategoryRepository = Depends(get_category_repository),
):
    return await categorypRepo.get_all(limit=limit, skip=skip)


@router.get("/group/", response_model=list[Category])
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
    current_user: User = Depends(get_current_user),
):
    groupRepo = get_group_repository()
    group = await groupRepo.get_by_id(data.group_id)
    if group:
        if current_user and group.creater == current_user.id:
            data = add_creater_field_to_dict(data.dict(), current_user.id)
            return await categorypRepo.create(d=data)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found group")


@router.patch("/", response_model=Category)
async def update_category(
    categoty_id: int,
    data: CategoryUpdate,
    categorypRepo: CategoryRepository = Depends(get_category_repository),
    current_user: User = Depends(get_current_user),
):
    if data.group_id is not None:
        groupRepo = get_group_repository()
        group = await groupRepo.get_by_id(data.group_id)
        if not group or group.creater != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
            )

    category = await categorypRepo.get_by_id(categoty_id)
    if current_user and category:
        if category.creater == current_user.id:
            data = dict_without_null_from_pydantic_model(data)
            return await categorypRepo.update(id=categoty_id, d=data)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found category"
    )


@router.delete("/")
async def delete_category(
    categoty_id: int,
    categorypRepo: CategoryRepository = Depends(get_category_repository),
    current_user: User = Depends(get_current_user),
):
    category = await categorypRepo.get_by_id(categoty_id)
    if current_user and category:
        if category.creater == current_user.id:
            return await categorypRepo.delete(id=categoty_id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found category"
    )
