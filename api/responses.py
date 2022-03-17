from typing import List
from pydantic import BaseModel


class Ingrediente(BaseModel):
    id: int
    item: str

    class Config:
	    orm_mode=True


class Item(BaseModel):
    secao: str
    conteudo: List[str]


class ItemComReceita(BaseModel):
    id: int
    item: str
    nome: str

    class Config:
	    orm_mode=True


class ReceitaCompleta(BaseModel):
    receita: str
    itens: List[Item]


class Receita(BaseModel):
    id: int
    nome: str

    class Config:
	    orm_mode=True
