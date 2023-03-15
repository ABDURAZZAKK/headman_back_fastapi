from databases import Database
from sqlalchemy import Table
from pydantic import BaseModel
from datetime import datetime



class BaseRepository:
    def __init__(self, database: Database,
                       db_model: Table,
                       return_model: BaseModel,
                        ) -> None:
        self.database = database
        self.db_model = db_model
        self.return_model = return_model


    async def get_all(self, limit: int = 100, skip: int = 0) -> list[BaseModel]:
        query = self.db_model.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_id(self, id: int) -> BaseModel | None:
        query = self.db_model.select().where(self.db_model.c.id==id)
        _ = await self.database.fetch_one(query)
        if _ is None: 
            return None
        return _
    

    async def create(self, d: BaseModel) -> BaseModel:
        new = self.return_model(
            **d.dict(),
            id=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new.dict()}
        values.pop('id', None)
        query = self.db_model.insert().values(**values)
        new.id = await self.database.execute(query)
        return new

    async def update(self, id: int, d: BaseModel) -> BaseModel | None:
        new = self.return_model(
            **d.dict(),
            id=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = self.db_model.update().where(self.db_model.c.id==id).values(**values)
        await self.database.execute(query)
        new.id = id 
        return new
            
        
    async def delete(self, id: int) -> None:
        query = self.db_model.delete().where(self.db_model.c.id==id)
        await self.database.execute(query)
        return {'id':id}