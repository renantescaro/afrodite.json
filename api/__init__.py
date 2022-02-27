from fastapi import FastAPI
from sqlalchemy import select
from models.banco import session_local
from models import ReceitaModel
from services.receita_sv import ReceitaSv

app = FastAPI()


@app.get('/receitas')
def todas_receitas():
    return session_local.execute(select(ReceitaModel)).scalars().all()


@app.get('/receitas/{id}')
def receita_por_id(id):
    return ReceitaSv().conteudos_por_receita_id(id)


@app.get('/receitas/{itens}')
def receita_por_itens(itens):
    return {'item_id': itens}
