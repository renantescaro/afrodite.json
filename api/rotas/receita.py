from typing import List
from api import app
from services.receita_sv import ReceitaSv
from api.responses import ReceitaCompleta, Receita


@app.get('/receitas', response_model=List[Receita], tags=['Receita'])
def todas_receitas():
    return ReceitaSv().lista_todas_receitas()


@app.get('/receitas/{id}', response_model=ReceitaCompleta, tags=['Receita'])
def receita_por_id(id:int):
    return ReceitaSv().lista_receitas_por_id(id)


@app.get('/receitas/ingrediente/{ingrediente}', response_model=List[Receita], tags=['Receita'])
def receitas_por_ingrediente(item:str):
    return ReceitaSv().lista_receitas_por_conteudo(item)
