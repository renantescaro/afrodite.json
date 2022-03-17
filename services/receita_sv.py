from sqlalchemy import select
from models.banco import session_local
from models import (ReceitaSecaoModel, ReceitaModel, SecaoModel, ConteudoModel, SecaoConteudoModel)


class ReceitaSv:
    def lista_todas_receitas(self):
        query = select(ReceitaModel)
        return session_local.execute(query).scalars().all()


    def receita_por_id(self, receita_id:int):
        receita_bd = session_local.execute(select(ReceitaModel).where(ReceitaModel.id == receita_id)).one()
        receita = dict(receita_bd)['ReceitaModel']

        receita_secoes = session_local.execute(
            select(ReceitaSecaoModel).
            where(ReceitaSecaoModel.id_receita == receita_id)
        ).scalars().all()

        receita_json = {'receita': receita.nome, 'itens': []}
        for receita_secao in receita_secoes:
            secao = session_local.execute(select(SecaoModel).where(SecaoModel.id == receita_secao.id_secao)).one()
            secao_model = dict(secao)['SecaoModel']

            query = select(SecaoConteudoModel).where(
                SecaoConteudoModel.id_secao == secao_model.id,
                SecaoConteudoModel.id_receita == receita.id
            )
            secao_conteudos = session_local.execute(query).scalars().all()

            conteudos = []
            for secao_conteudo in secao_conteudos:
                conteudo = session_local.execute(select(ConteudoModel).where(ConteudoModel.id == secao_conteudo.id)).one()
                conteudos.append(dict(conteudo)['ConteudoModel'].item)

            receita_json['itens'].append({
                'secao' : secao_model.nome,
                'conteudo' : conteudos
            })

        return receita_json


    def lista_receitas_por_conteudo(self, item:str):
        query = session_local.query(
            ReceitaModel.id,
            ReceitaModel.nome,
            ConteudoModel.item
        ).\
        select_from(SecaoConteudoModel).\
        join(ConteudoModel).\
        filter(
            SecaoConteudoModel.id_secao == 1,
            SecaoConteudoModel.id_receita == ReceitaModel.id,
            ConteudoModel.item.like('%{}%'.format(item))
        ).\
        group_by(ReceitaModel.id).\
        limit(100)

        return session_local.execute(query).mappings().all()


    def lista_receitas_por_nome(self, nome:str):
        query = select(
            ReceitaModel
        ).\
        where(
            ReceitaModel.nome.like('%{}%'.format(nome))
        ).\
        limit(100)

        return session_local.execute(query).scalars().all()
