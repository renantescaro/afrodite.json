import json
from typing import Any, List
from entidades import Receita, Secao, Conteudo
from models import ReceitaModel, SecaoModel, ConteudoModel
from models.banco import session_local
from models.receita_secao_model import ReceitaSecaoModel
from models.secao_conteudo_model import SecaoConteudoModel


def salvar_receitas():
    for receita in _montar_receitas():
        receita_model = ReceitaModel(
            nome=receita.nome
        )
        session_local.add(receita_model)
        session_local.commit()
        session_local.refresh(receita_model)

        for secao in receita.secao:
            secao_model = SecaoModel(
                nome=secao.nome
            )
            session_local.add(secao_model)
            session_local.commit()
            session_local.refresh(secao_model)

            receita_secao_model = ReceitaSecaoModel(
                id_receita=receita_model.id,
                id_secao=secao_model.id
            )
            session_local.add(receita_secao_model)
            session_local.commit()
            session_local.refresh(receita_secao_model)

            for conteudo in secao.conteudo:
                conteudo_model = ConteudoModel(
                    item=conteudo.item
                )
                session_local.add(conteudo_model)
                session_local.commit()
                session_local.refresh(conteudo_model)

                secao_conteudo_model = SecaoConteudoModel(
                    id_conteudo=conteudo_model.id,
                    id_secao=secao_model.id
                )
                session_local.add(secao_conteudo_model)
                session_local.commit()
                session_local.refresh(secao_conteudo_model)


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


def _montar_receitas() -> List[Receita]:
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
