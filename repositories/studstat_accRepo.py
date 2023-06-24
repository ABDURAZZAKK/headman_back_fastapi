import sqlalchemy as sa
from db.models import studstat_accs
from .baseRepo import BaseRepository


class StudstatAccRepository(BaseRepository):
    async def get_by_user_id(self, u_id: int):
        query = sa.select(studstat_accs).where(studstat_accs.c.user_id == u_id)
        _ = await self.session.execute(query)
        _ = _.fetchone()

        if _ is None:
            return None
        return _
