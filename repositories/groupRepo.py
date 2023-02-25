from datetime import datetime

from models.group import Group, GroupIn
from db.models import groups
from .baseRepo import BaseRepository


class GroupRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[Group]:
        query = groups.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_id(self, id: int) -> Group | None:
        query = groups.select().where(groups.c.id==id)
        group_ = await self.database.fetch_one(query)
        if group_ is None: 
            return None
        return group_

    
    async def create(self, d: GroupIn) -> Group:
        new_group = Group(
            id=0,
            name=d.name,
            headman=d.headman,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_group.dict()}
        values.pop('id', None)
        query = groups.insert().values(**values)
        new_group.id = await self.database.execute(query)
        return new_group

    async def update(self, id: int, d: GroupIn) -> Group | None:
        new_group = Group(
            id=0,
            name=d.name,
            headman=d.headman,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_group.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = groups.update().where(groups.c.id==id).values(**values)
        await self.database.execute(query)
        new_group.id = id 
        return new_group
            
        
    async def delete(self, id: int) -> None:
        query = groups.delete().where(groups.c.id==id)
        await self.database.execute(query)
        return {'id':id}
         
        