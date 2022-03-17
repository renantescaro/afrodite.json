from api import app
from services.conteudo_sv import IngredienteSv
from api.responses import Ingrediente
from fastapi_pagination import Page, paginate, add_pagination


@app.get('/ingredientes', response_model=Page[Ingrediente], tags=['Ingrediente'])
async def todos_ingredientes():
    return paginate(IngredienteSv().lista_todos_ingredientes())


@app.get('/ingredientes/busca/{item}', response_model=Page[Ingrediente], tags=['Ingrediente'])
async def busca_ingrediente_por_nome(item:str):
    return paginate(IngredienteSv().lista_ingredientes_por_nome(item))


add_pagination(app)
