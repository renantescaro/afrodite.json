from typing import List
from entidades.secao import Secao

class Receita:
    def __init__(self, nome:str, secao:List[Secao]) -> None:
        self.nome = nome
        self.secao = secao
