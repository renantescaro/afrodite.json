from typing import Any, List, Optional
from sqlalchemy import select
import logging
from entidades import Receita, Secao, Conteudo
from models import ReceitaModel, SecaoModel, ConteudoModel, conteudo_model
from models.banco import session_local
from models.receita_secao_model import ReceitaSecaoModel
from models.secao_conteudo_model import SecaoConteudoModel
from services.ler_json import LerJson

logging.basicConfig(filename='importar_json.log', encoding='utf-8', level=logging.DEBUG)


def _salvar_bd(model):
    session_local.add(model)
    session_local.commit()
    session_local.refresh(model)
    return model


def _id_secao_por_nome(nome_secao:str, secoes_padrao) -> int:
    if nome_secao == 'Ingredientes':
        return int(secoes_padrao[0]['id'])
    elif nome_secao == 'Modo de Preparo':
        return int(secoes_padrao[1]['id'])
    elif nome_secao == 'Outras informações':
        return int(secoes_padrao[2]['id'])


def _limpar_texto(texto:str) -> str:
    sujeira = ['•', '·', '–', '-', '*', '**']
    texto = texto.lstrip()
    logging.info(texto)
    if texto[0] in sujeira:
        return texto[2:].lstrip() if texto[1] in sujeira else texto[1:].lstrip()
    return texto


def _texto_valido(texto:str) -> bool:
    texto = ''.join(texto.split())
    if len(texto) <= 0:
        return False

    texto = _limpar_texto(texto).lower()
    remover = [
        'vejatambém:',
        'vejatambém:falsopasteldepão',
        'vejatambém:receitadefarofadoce',
        'www.facebook.com/enjoycanola',
        'confiratambém:'
    ]
    if texto in remover:
        return False
    return True


def _salvar_secoes() -> list[dict[str, Any]]:
    secoes_padrao = [
        {'nome':'Ingredientes', 'id':None},
        {'nome':'Modo de Preparo', 'id':None},
        {'nome':'Outras informações', 'id':None},
    ]
    for secao in secoes_padrao:
        secao_model = SecaoModel(
            nome=secao['nome']
        )
        secao_model = _salvar_bd(secao_model)

        secao['id'] = secao_model.id
    return secoes_padrao


def _salvar_conteudo(conteudo:ConteudoModel) -> Optional[ConteudoModel]:
    if not _texto_valido(conteudo.item):
        return None

    conteudo.item = _limpar_texto(conteudo.item)
    conteudo_busca = session_local.execute(select(ConteudoModel).where(ConteudoModel.item == conteudo.item)).first()

    conteudo_model = None
    if conteudo_busca is not None:
        conteudo_model = dict(conteudo_busca)['ConteudoModel']

    if conteudo_model is None:
        conteudo_model = ConteudoModel(
            item=conteudo.item
        )
        return _salvar_bd(conteudo_model)


def _salvar_receita_secao(receita_model:ReceitaModel, secao_id:int) -> ReceitaSecaoModel:
    receita_secao_model = ReceitaSecaoModel(
        id_receita=receita_model.id,
        id_secao=secao_id
    )
    return _salvar_bd(receita_secao_model)


def _salvar_secao_conteudo(receita_id:int, secao_id:int, conteudo_id:int) -> SecaoConteudoModel:
    secao_conteudo_model = SecaoConteudoModel(
        id_conteudo=conteudo_id,
        id_receita=receita_id,
        id_secao=secao_id
    )
    return _salvar_bd(secao_conteudo_model)


def salvar_receitas():
    receitas = LerJson().ler()
    secoes_padrao = _salvar_secoes()

    for receita in receitas:
        receita_model = ReceitaModel(
            nome=receita.nome
        )
        receita_model = _salvar_bd(receita_model)

        for secao in receita.secao:
            secao_id = _id_secao_por_nome(secao.nome, secoes_padrao)

            _salvar_receita_secao(receita_model, secao_id)

            for conteudo in secao.conteudo:
                conteudo_model = _salvar_conteudo(conteudo)

                if conteudo_model is not None:
                    _salvar_secao_conteudo(
                        receita_id=receita_model.id,
                        secao_id=secao_id,
                        conteudo_id=conteudo_model.id
                    )
