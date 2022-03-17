from api import app
from services.receita_sv import ReceitaSv
from api.responses import ItemComReceita, ReceitaCompleta, Receita
from fastapi_pagination import Page, paginate, add_pagination


@app.get('/receitas', response_model=Page[Receita], tags=['Receita'])
def todas_receitas():
    return paginate(ReceitaSv().lista_todas_receitas())


@app.get('/receitas/{id}', response_model=ReceitaCompleta, tags=['Receita'])
def receita_por_id(id:int):
    return ReceitaSv().receita_por_id(id)


@app.get('/receitas/busca/{nome}', response_model=Page[Receita], tags=['Receita'])
def busca_receitas_por_nome(nome:str):
    return paginate(ReceitaSv().lista_receitas_por_nome(nome))


@app.get('/receitas/ingrediente/busca/{item}', response_model=Page[ItemComReceita], tags=['Receita'])
def busca_receitas_por_ingrediente(item:str):
    return paginate(ReceitaSv().lista_receitas_por_conteudo(item))


add_pagination(app)
