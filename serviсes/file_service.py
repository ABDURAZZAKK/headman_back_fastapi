import os
import shutil
from datetime import datetime
from fastapi import File
from core.config import HW_ATTACHED_PATH


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

def delete_hw_attached_files(path_to_files: str) -> None:
    for file in os.listdir(path_to_files):
        os.remove(f'{path_to_files}\\{file}')

def rmdir_hw_attached_files(path_to_files: str) -> None:
    shutil.rmtree(path_to_files)
    