from datetime import datetime
from core.config import HW_ATTACHED_PATH
from models.homework import Homework, HomeworkIn
from db.models import homeworks
from .baseRepo import BaseRepository



class HomeworkRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[Homework] | None:
        query = homeworks.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_category_id(self, category_id, limit: int = 100, skip: int = 0) -> list[Homework] | None:
        query = homeworks.select().where(homeworks.c.category_id==category_id).limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_id(self, id: int) -> Homework | None:
        query = homeworks.select().where(homeworks.c.id==id)
        homework_ = await self.database.fetch_one(query)
        if homework_ is None: 
            return None
        return homework_ 

    async def create(self, d: HomeworkIn) -> Homework:
        new_homework = Homework(
            id=0,
            task=d.task,
            status=d.status,
            path_to_files=d.path_to_files,
            category_id=d.category_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        values = {**new_homework.dict()}
        values.pop('id', None)
        query = homeworks.insert().values(**values)
        new_homework.id = await self.database.execute(query)
        return new_homework

    async def update(self, id: int, d: HomeworkIn) -> Homework | None:
        new_homework = Homework(
            id=0,
            task=d.task,
            status=d.status,
            path_to_files=d.path_to_files,
            category_id=d.category_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        values = {**new_homework.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        values.pop("path_to_files", None)
        query = homeworks.update().where(homeworks.c.id==id).values(**values)
        await self.database.execute(query)
        new_homework.id = id
        return new_homework
            
            
    async def delete(self, id: int) -> None:
        query = homeworks.delete().where(homeworks.c.id==id)
        await self.database.execute(query)
        return {'id': id}
         
        