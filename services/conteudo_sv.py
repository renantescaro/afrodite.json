from sqlalchemy import select
from models.banco import session_local
from models import (ConteudoModel)


class IngredienteSv:
    def lista_todos_ingredientes(self):
        query = select(ConteudoModel)
        return session_local.execute(query).scalars().all()


    def lista_ingredientes_por_nome(self, ingrediente:str):
        query = select(
            ConteudoModel
        ).\
        where(
            ConteudoModel.item.like('%{}%'.format(ingrediente))
        ).\
        limit(100)

        return session_local.execute(query).scalars().all()
