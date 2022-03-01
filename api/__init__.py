from typing import List
from fastapi import FastAPI
from services.receita_sv import ReceitaSv
from .responses import ReceitaCompleta, Receita

app = FastAPI(title='Api Receitas')


@app.get('/receitas', response_model=List[Receita])
def todas_receitas():
    return ReceitaSv().lista_todas_receitas()


@app.get('/receitas/{id}', response_model=ReceitaCompleta)
def receita_por_id(id:int):
    return ReceitaSv().lista_receitas_por_id(id)


@app.get('/receitas/item/{item}', response_model=List[Receita])
def receitas_por_item(item:str):
    return ReceitaSv().lista_receitas_por_conteudo(item)
