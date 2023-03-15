from models.homework import Homework
from db.models import homeworks
from .baseRepo import BaseRepository



class HomeworkRepository(BaseRepository):
     
    async def get_by_category_id(self, category_id, limit: int = 100, skip: int = 0) -> list[Homework] | None:
        query = homeworks.select().where(homeworks.c.category_id==category_id).limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    

        