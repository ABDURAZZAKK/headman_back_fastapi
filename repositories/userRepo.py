from datetime import datetime

from core.security import hash_password
from models.user import User, UserIn
from db.models import users
from .baseRepo import BaseRepository


class UserRepository(BaseRepository):

    async def get_by_email(self, email: str) -> User | None:
        query = users.select().where(users.c.email==email)
        user_ = await self.database.fetch_one(query)
        if user_ is None: 
            return None
        return user_
    
    async def create(self, d: UserIn) -> User:
        new_user = User(
            id=0,
            name=d.name,
            email=d.email,
            hashed_password=hash_password(d.password2),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_user.dict()}
        values.pop('id', None)
        query = users.insert().values(**values)
        new_user.id = await self.database.execute(query)
        return new_user

    async def update(self, id: int, d: UserIn) -> User | None:
        new_user = User(
            id=0,
            name=d.name,
            email=d.email,
            hashed_password=hash_password(d.password2),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_user.dict()}
        values.pop('id', None)
        values.pop("created_at", None)
        query = users.update().where(users.c.id==id).values(**values)
        await self.database.execute(query)
        new_user.id = id
        return new_user
            
         
        