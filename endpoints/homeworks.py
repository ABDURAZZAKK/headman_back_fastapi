import os

from fastapi import APIRouter, Depends,  UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse

from repositories.homeworkRepo import HomeworkRepository
from .depends import get_current_user, get_homework_repository, get_category_repository, get_group_repository
from models.user import User
from models.homework import Homework, HomeworkIn
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


@router.post("/", response_model=Homework)
async def create_hw(
        data: HomeworkIn,
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user),
        ):
    categoryRepo = get_category_repository()
    category = await categoryRepo.get_by_id(data.category_id)
    if current_user and category:
        groupRepo = get_group_repository()
        group = await groupRepo.get_by_id(category.group_id)
        if group and group.headman == current_user.id:
            path = file_service.create_timestamp_dir()
            data.path_to_files = path
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
        categoryRepo = get_category_repository()
        category = await categoryRepo.get_by_id(hw.category_id)
        if category:
            groupRepo = get_group_repository()
            group = await groupRepo.get_by_id(category.group_id)
            if group and group.headman == current_user.id:
                try:

                    for file in files:
                        mb = 1024*1024
                        filename = file.filename
                        file_context = await file.read(11*mb)
                        if len(file_context) >= 10*mb:
                            
                            file_service.delete_hw_attached_files(hw.path_to_files)
                            raise HTTPException(status.HTTP_403_FORBIDDEN)
                        file_service.save_file_context(hw.path_to_files, file_context, filename)

                    return JSONResponse({'status': 'OK'})
                
                except HTTPException:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your file is more than 10MB")
                except:
                    file_service.delete_hw_attached_files(hw.path_to_files)
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='File upload error')
                
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")


# @router.patch("/", response_model=Homework)
# async def update_hw(
#         hw_id: int,
#         data: HomeworkIn,
#         hwRepo: HomeworkRepository = Depends(get_homework_repository),
#         current_user: User = Depends(get_current_user)):
    
#     hw = await hwRepo.get_by_id(hw_id)
#     if current_user and hw:
#         categoryRepo = get_category_repository()
#         category = await categoryRepo.get_by_id(hw.category_id)
#         if category:
#             groupRepo = get_group_repository()
#             group = await groupRepo.get_by_id(category.group_id)
#             if group and group.headman == current_user.id:
#                 return await hwRepo.update(id=hw_id, d=data)
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")
    

@router.delete("/")
async def delete_hw(
        hw_id: int,
        hwRepo: HomeworkRepository = Depends(get_homework_repository),
        current_user: User = Depends(get_current_user)):

    hw = await hwRepo.get_by_id(hw_id)
    if current_user and hw:
        categoryRepo = get_category_repository()
        category = await categoryRepo.get_by_id(hw.category_id)
        if category:
            groupRepo = get_group_repository()
            group = await groupRepo.get_by_id(category.group_id)
            if group and group.headman == current_user.id:
                file_service.rmdir_hw_attached_files(hw.path_to_files)
                return await hwRepo.delete(id=hw_id)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access is denied")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found homework")