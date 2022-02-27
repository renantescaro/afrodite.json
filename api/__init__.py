from typing import List
from fastapi import FastAPI
from sqlalchemy import select
from models.banco import session_local
from models import ReceitaModel
from services.receita_sv import ReceitaSv
from .responses import ReceitaCompleta, Receita

app = FastAPI()


@app.get('/receitas', response_model=List[Receita])
def todas_receitas():
    return session_local.execute(select(ReceitaModel)).scalars().all()


@app.get('/receitas/{id}', response_model=ReceitaCompleta)
def receita_por_id(id:int):
    return ReceitaSv().conteudos_por_receita_id(id)


@app.get('/receitas/{itens}', response_model=List[ReceitaCompleta])
def receita_por_itens(itens:str):
    return {'item_id': itens}
