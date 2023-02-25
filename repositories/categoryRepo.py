from datetime import datetime

from models.category import Category, CategoryIn
from db.models import categories
from .baseRepo import BaseRepository


class CategoryRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[Category]:
        query = categories.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_group_id(self, group_id, limit: int = 100, skip: int = 0) -> list[Category] | None:
        query = categories.select().where(categories.c.group_id==group_id).limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_id(self, id: int) -> Category | None:
        query = categories.select().where(categories.c.id==id)
        category_ = await self.database.fetch_one(query)
        if category_ is None: 
            return None
        return category_

    
    async def create(self, d: CategoryIn) -> Category:
        new_category = Category(
            id=0,
            name=d.name,
            group_id=d.group_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_category.dict()}
        values.pop('id', None)
        query = categories.insert().values(**values)
        new_category.id = await self.database.execute(query)
        return new_category

    async def update(self, id: int, d: CategoryIn) -> Category | None:
        new_category = Category(
            id=0,
            name=d.name,
            group_id=d.group_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_category.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = categories.update().where(categories.c.id==id).values(**values)
        await self.database.execute(query)
        new_category.id = id
        return new_category
            
        
    async def delete(self, id: int) -> None:
        query = categories.delete().where(categories.c.id==id)
        await self.database.execute(query)
        return {'id':id}
         
        