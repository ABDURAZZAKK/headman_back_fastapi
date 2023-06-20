from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from pydantic import BaseModel
from datetime import datetime

M = TypeVar("M", bound=BaseModel)


class BaseRepository:
    def __init__(
        self,
        session: AsyncSession,
        db_model,
        return_model: M,
    ) -> None:
        self.session = session
        self.db_model = db_model
        self.return_model = return_model

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[M]:
        query = sa.select(self.db_model).limit(limit).offset(skip)
        result = await self.session.execute(query)

        return result.all()

    async def get_by_id(self, id: int) -> M | None:
        query = sa.select(self.db_model).where(self.db_model.c.id == id)
        _ = await self.session.execute(query)
        _ = _.fetchone()

        if _ is None:
            return None
        return _

    async def create(self, d: M | dict) -> M:
        new = self.return_model(
            **dict(d),
            id=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        values = {**new.dict()}
        values.pop("id", None)
        query = sa.insert(self.db_model).values(**values).returning(self.db_model.c.id)
        new_id = await self.session.execute(query)
        new.id = new_id.fetchone()[0]
        await self.session.commit()
        return new

    async def update(self, id: int, d: dict) -> None:
        d["updated_at"] = datetime.utcnow()
        query = self.db_model.update().where(self.db_model.c.id == id).values(**d)
        await self.session.execute(query)
        await self.session.commit()
        return {"status": "success"}

    async def delete(self, id: int) -> None:
        query = self.db_model.delete().where(self.db_model.c.id == id)
        await self.session.execute(query)
        await self.session.commit()
        return {"status": "success"}
