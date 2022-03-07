import json
from typing import Any, List
from entidades import Receita, Secao, Conteudo
from models import ReceitaModel, SecaoModel, ConteudoModel
from models.banco import session_local
from models.receita_secao_model import ReceitaSecaoModel
from models.secao_conteudo_model import SecaoConteudoModel


def _salvar_secoes():
    secoes_padrao = [
        {'nome':'Ingredientes', 'id':None},
        {'nome':'Modo de Preparo', 'id':None},
        {'nome':'Outras informações', 'id':None},
    ]
    for secao in secoes_padrao:
        secao_model = SecaoModel(
            nome=secao['nome']
        )
        session_local.add(secao_model)
        session_local.commit()
        session_local.refresh(secao_model)

        secao['id'] = secao_model.id
    return secoes_padrao


def _id_secao_por_nome(nome_secao:str, secoes_padrao) -> int:
    if nome_secao == 'Ingredientes':
        return int(secoes_padrao[0]['id'])
    elif nome_secao == 'Modo de Preparo':
        return int(secoes_padrao[1]['id'])
    elif nome_secao == 'Outras informações':
        return int(secoes_padrao[2]['id'])


def _limpar_texto(texto:str) -> str:
    texto = texto.lstrip()
    if texto[0] in ['•', '·', '–', '-', '*']:
        return texto[1:].lstrip()
    return texto


def _texto_valido(texto:str) -> bool:
    if len(''.join(texto.lstrip())) <= 0:
        return False

    remover = ['   VEJA TAMBÉM:', '  VEJA TAMBÉM: ', '   CONFIRA TAMBÉM:']
    if texto in remover:
        return False
    return True
    

def salvar_receitas():
    secoes_padrao = _salvar_secoes()

    for receita in _montar_receitas():
        # salva receita
        receita_model = ReceitaModel(
            nome=receita.nome
        )
        session_local.add(receita_model)
        session_local.commit()
        session_local.refresh(receita_model)

        for secao in receita.secao:
            secao_id = _id_secao_por_nome(secao.nome, secoes_padrao)

            # salva receita seção
            receita_secao_model = ReceitaSecaoModel(
                id_receita=receita_model.id,
                id_secao=secao_id
            )
            session_local.add(receita_secao_model)
            session_local.commit()
            session_local.refresh(receita_secao_model)

            for conteudo in secao.conteudo:
                # salva conteúdo
                
                if _texto_valido(conteudo.item):
                    conteudo.item = _limpar_texto(conteudo.item)

                    conteudo_model = ConteudoModel(
                        item=conteudo.item
                    )
                    session_local.add(conteudo_model)
                    session_local.commit()
                    session_local.refresh(conteudo_model)

                    # salva seção conteúdo
                    secao_conteudo_model = SecaoConteudoModel(
                        id_conteudo=conteudo_model.id,
                        id_secao=secao_id
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
        # remove primeiro caracter se este for em branco
        secao_nome = secao['nome'][1:] if secao['nome'][0] == ' ' else secao['nome']

        conteudos_list = _montar_conteudos(secao['conteudo'])
        secao_obj = Secao(
            nome=secao_nome,
            conteudo=conteudos_list
        )
        secoes_list.append(secao_obj)
    return secoes_list


def _montar_receitas() -> List[Receita]:
    receitas_arquivo = open('static/afrodite.json', encoding='utf8')
    receitas = json.load(receitas_arquivo)

    receitas_list = []
    for receita in receitas:
        secoes_list = _montar_secoes(receita['secao'])

        receita_obj = Receita(
            nome=receita['nome'],
            secao=secoes_list
        )
        receitas_list.append(receita_obj)
    return receitas_list
