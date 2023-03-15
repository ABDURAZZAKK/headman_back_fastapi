from datetime import datetime

from fastapi import HTTPException, status

from models.studstat_acc import StudstatAcc, StudstatAccIn 
from db.models import studstat_accs
from .baseRepo import BaseRepository

from serviсes import points_parser

class StudstatAccRepository(BaseRepository):

    async def get_by_user_id(self, user_id: int) -> StudstatAcc | None:
        query = studstat_accs.select().where(studstat_accs.c.user_id==user_id)
        studstat_acc_ = await self.database.fetch_one(query)
        if studstat_acc_ is None: 
            return None
        return studstat_acc_


    def _registration(data):
        data = {
            "Input.lastname": data.lastname,
            "Input.firstname": data.firstname,
            "Input.patr": data.patr,
            "Input.nbook": data.nbook,
            }
        
        response = points_parser.registration(data)

        return response

    async def create(self, d: StudstatAccIn) -> StudstatAcc:
        
        if self._registration(d).status_code == 200:
            new_studstat_acc = StudstatAcc(
                id=0,
                lastname=d.lastname,
                firstname=d.firstname,
                patr=d.patr,
                nbook=d.nbook,
                user_id=d.user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            
            values = {**new_studstat_acc.dict()}
            values.pop('id', None)
            query = studstat_accs.insert().values(**values)
            new_studstat_acc.id = await self.database.execute(query)
            return new_studstat_acc
        
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data")


    async def update(self, id: int, d: StudstatAccIn) -> StudstatAcc | None:

        if self._registration(d).status_code == 200:
            new_studstat_acc = StudstatAcc(
                    id=0,
                    lastname=d.lastname,
                    firstname=d.firstname,
                    patr=d.patr,
                    nbook=d.nbook,
                    user_id=d.user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )

            values = {**new_studstat_acc.dict()}
            values.pop('id', None)
            values.pop("created_at", None)
            query = studstat_accs.update().where(studstat_accs.c.id==id).values(**values)
            await self.database.execute(query)
            new_studstat_acc.id = id
            return new_studstat_acc
                

         
        