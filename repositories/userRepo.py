from datetime import datetime
import sqlalchemy as sa
from core.security import hash_password
from models.user import User, UserIn
from db.models import users

from .baseRepo import BaseRepository


class UserRepository(BaseRepository):
    async def get_by_email(self, email: str) -> User | None:
        query = sa.select(users).where(users.c.email == email)
        _ = await self.session.execute(query)
        _ = _.fetchone()

        if _ is None:
            return None
        return _

    async def create(self, d: UserIn | dict) -> User:
        d = dict(**dict(d))
        new_user = User(
            id=0,
            name=d["name"],
            email=d["email"],
            hashed_password=hash_password(d["password2"]),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new_user.dict()}
        values.pop("id", None)
        query = sa.insert(users).values(**values).returning(users.c.id)
        user_id = await self.session.execute(query)
        new_user.id = user_id.fetchone()[0]
        await self.session.commit()

        return new_user

    async def update(self, id: int, d: UserIn | dict) -> User | None:
        d = dict(**dict(d))

        if "password2" in d:
            d["hashed_password"] = hash_password(d["password2"])
            del d["password2"]
            del d["password"]
        d["updated_at"] = datetime.utcnow()

        query = sa.update(users).where(users.c.id == id).values(**d)
        await self.session.execute(query)
        await self.session.commit()
        return {"status": "success"}
