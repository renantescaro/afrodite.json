from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    secao: str
    conteudo: List[str]


class ReceitaCompleta(BaseModel):
    receita: str
    itens: List[Item]


class Receita(BaseModel):
    id: int
    nome: str

    class Config:
	    orm_mode=True

