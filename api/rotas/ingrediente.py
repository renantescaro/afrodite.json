from api import app
from services.conteudo_sv import IngredienteSv


@app.get('/ingredientes', tags=['Ingrediente'])
def todos_ingredientes():
    return IngredienteSv().lista_todos_ingredientes()


@app.get('/ingredientes/{ingrediente}', tags=['Ingrediente'])
def ingrediente_por_nome(ingrediente:str):
    return IngredienteSv().lista_ingredientes_por_nome(ingrediente)
