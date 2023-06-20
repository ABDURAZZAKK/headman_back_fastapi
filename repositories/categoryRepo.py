from models.category import Category
from db.models import categories
from .baseRepo import BaseRepository
import sqlalchemy as sa


class CategoryRepository(BaseRepository):
    async def get_by_group_id(
        self, group_id, limit: int = 100, skip: int = 0
    ) -> list[Category] | None:
        query = (
            sa.select(categories)
            .where(categories.c.group_id == group_id)
            .limit(limit)
            .offset(skip)
        )
        result = await self.session.execute(query=query)
        return result.all()
