from typing import List
from entidades.conteudo import Conteudo


class Secao:
    def __init__(self, nome:str, conteudo:List[Conteudo]) -> None:
        self.nome = nome
        self.conteudo = conteudo
