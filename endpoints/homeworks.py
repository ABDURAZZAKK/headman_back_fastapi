import os

from fastapi import APIRouter, Depends,  UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse

from repositories.homeworkRepo import HomeworkRepository
from .depends import get_current_user, get_homework_repository, get_category_repository
from .utils import add_creater_field_to_dict, delete_none_from_pydantic_model
from models.user import User
from models.homework import Homework, HomeworkIn, HomeworkUpdate
from serviсes import file_service
from core.config import HW_ATTACHED_PATH

router = APIRouter()


@router.get("/all", response_model=list[Homework])
async def get_hws(
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        limit: int = 100,
        skip: int = 0):

    return await hwRepo.get_all(limit=limit, skip=skip)


@router.get("/category/{category_id}", response_model=list[Homework])
async def get_hws_by_category_id(
        category_id: int,
        hwRepo: HomeworkRepository = Depends(get_homework_repository)):

    return await hwRepo.get_by_category_id(category_id)


@router.get('/attached_files/{hw_id}')
async def get_attached_file_names(hw_id: int, 
                             hwRepo: HomeworkRepository = Depends(get_homework_repository)):
    hw = await hwRepo.get_by_id(hw_id)
    if hw: 
        return {'file_names': os.listdir(hw.path_to_files)} 
    

@router.get('/file/{dir_path}/{file_name}', response_class=FileResponse)
async def get_file(dir_path: int, file_name: str):
    file_name = file_name.replace('\\','').replace('/','')
    return FileResponse(f'{HW_ATTACHED_PATH}\\{dir_path}\\{file_name}', 
                    filename=file_name,
                    media_type="multipart/form-data")


@router.delete('/file/{hw_id}/{file_name}')
async def delete_file(hw_id: int,
                      file_name: str,
                      hwRepo: HomeworkRepository = Depends(get_homework_repository),
                      current_user: User = Depends(get_current_user),):
    hw = await hwRepo.get_by_id(hw_id)
    if current_user and hw:
        if hw.creater == current_user.id:

            file_name = file_name.replace('\\','').replace('/','')
            path = f'{hw.path_to_files}\\{file_name}'
            if os.path.exists(path):
                os.remove(path)
                return JSONResponse({'status': status.HTTP_200_OK})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')


@router.post("/", response_model=Homework)
async def create_hw(
        data: HomeworkIn,
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user),
        ):
    categoryRepo = get_category_repository()
    category = await categoryRepo.get_by_id(data.category_id)
    if current_user and category:
        if category.creater == current_user.id:
            data = add_creater_field_to_dict(data.dict(), current_user.id)
            return await hwRepo.create(d=data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found category")
    

@router.post("/attaching_file", response_class=JSONResponse)
async def attach_hw_file(
        hw_id: int,
        files: list[UploadFile],
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user),
        ):
    
    hw = await hwRepo.get_by_id(hw_id)
    if current_user and hw:
        if hw.creater == current_user.id:
            if hw.path_to_files is None:
                await hwRepo.update(hw.id, d = {'path_to_files': file_service.create_timestamp_dir()})
                hw = await hwRepo.get_by_id(hw_id)
            return await file_service.save_files(files, hw)
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")


@router.patch("/", response_model=Homework)
async def update_hw(
        hw_id: int,
        data: HomeworkUpdate,
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user)):
    
    if data.category_id is not None:
        categoryRepo = get_category_repository()
        category = await categoryRepo.get_by_id(data.category_id)
        if not category or  category.creater != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    
    hw = await hwRepo.get_by_id(hw_id)
    if current_user and hw:
        if hw.creater == current_user.id:
            data = delete_none_from_pydantic_model(data)
            return await hwRepo.update(id=hw_id, d=data)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")
    

@router.delete("/")
async def delete_hw(
        hw_id: int,
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user)):

    hw = await hwRepo.get_by_id(hw_id)
    if current_user and hw:
        if hw.creater == current_user.id:
            file_service.rmdir_hw_attached_files(hw.path_to_files)
            return await hwRepo.delete(id=hw_id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")