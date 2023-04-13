import os
import shutil
from datetime import datetime
from fastapi import File
from core.config import HW_ATTACHED_PATH
from fastapi import  HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from models.homework import Homework


async def save_files(files: list[UploadFile], hw: Homework) -> JSONResponse:
    try:
        for file in files:
            mb = 1024*1024
            filename = file.filename
            file_context = await file.read(11*mb)
            if len(file_context) >= 10*mb:
                
                delete_request_hw_attached_files(hw.path_to_files, files)
                raise HTTPException(status.HTTP_403_FORBIDDEN)
            save_file_context(hw.path_to_files, file_context, filename)

        return JSONResponse({'status': status.HTTP_201_CREATED})
    
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your file is more than 10MB")
    except:
        delete_request_hw_attached_files(hw.path_to_files, files)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='File upload error')


def delete_file(path_to_file: str, file_name: str) -> JSONResponse:
    file_name = file_name.replace('\\','').replace('/','')
    path = f'{path_to_file}\\{file_name}'
    if os.path.exists(path):
        os.remove(path)
        return JSONResponse({'status': status.HTTP_200_OK})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')


def create_timestamp_dir() -> str:
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))

    path = f'{HW_ATTACHED_PATH}\\{timestamp}'
    os.mkdir(path)

    return path
    
    
def save_file_context(path: str, file_context, filename: str) -> None:
    with open(f'{path}\\{filename}', 'wb') as f:
        f.write(file_context)
        f.close()


def delete_request_hw_attached_files(path_to_files: str, files: list[UploadFile]) -> None:
    filenames = [file.filename for file in files]
    for file in os.listdir(path_to_files):
        if file in filenames:
            os.remove(f'{path_to_files}\\{file}')


def rmdir_hw_attached_files(path_to_files: str) -> None:
    shutil.rmtree(path_to_files)



    