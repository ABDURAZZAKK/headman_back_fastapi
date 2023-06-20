from models.homework import Homework
from db.models import homeworks

from .baseRepo import BaseRepository
import sqlalchemy as sa


class HomeworkRepository(BaseRepository):
    async def get_by_category_id(
        self, category_id, limit: int = 100, skip: int = 0
    ) -> list[Homework] | None:
        query = (
            sa.select(homeworks)
            .where(homeworks.c.category_id == category_id)
            .limit(limit)
            .offset(skip)
        )
        result = await self.session.execute(query=query)
        return result.all()
