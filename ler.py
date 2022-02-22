import json
from typing import Any, List
from entidades import Receita, Secao, Conteudo


def _montar_conteudos(conteudos:Any) -> List[Conteudo]:
    conteudos_list = []
    for conteudo in conteudos:
        conteudo_obj = Conteudo(
            item=conteudo
        )
        conteudos_list.append(conteudo_obj)
    return conteudos_list


def _montar_secoes(secoes:Any) -> List[Secao]:
    secoes_list = []
    for secao in secoes:
        conteudos_list = _montar_conteudos(secao['conteudo'])
        secao_obj = Secao(
            nome=secao['nome'],
            conteudo=conteudos_list
        )
        secoes_list.append(secao_obj)
    return secoes_list


def montar_receitas() -> List[Receita]:
    receitas_arquivo = open('afrodite.json', encoding='utf8')
    receitas = json.load(receitas_arquivo)

    # receitas
    receitas_list = []
    for receita in receitas:
        secoes_list = _montar_secoes(receita['secao'])

        receita_obj = Receita(
            nome=receita['nome'],
            secao=secoes_list
        )
        receitas_list.append(receita_obj)
    return receitas_list


for receita in montar_receitas():
    print(receita.nome)
    if len(receita.secao[0].conteudo) > 0:
        print(receita.secao[0].conteudo[0].item)

    print('------------')
