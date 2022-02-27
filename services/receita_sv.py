from sqlalchemy import select
from models.banco import session_local
from models import (ReceitaSecaoModel, ReceitaModel, SecaoModel, ConteudoModel, SecaoConteudoModel)


class ReceitaSv:
    def conteudos_por_receita_id(self, receita_id:int):
        receita = session_local.execute(select(ReceitaModel).where(ReceitaModel.id == receita_id)).one()
        receita_nome = dict(receita)['ReceitaModel'].nome

        receita_secoes = session_local.execute(
            select(ReceitaSecaoModel).
            where(ReceitaSecaoModel.id_receita == receita_id)
        ).scalars().all()

        receita_json = {'receita': receita_nome, 'itens': []}
        for receita_secao in receita_secoes:
            secao = session_local.execute(select(SecaoModel).where(SecaoModel.id == receita_secao.id)).one()
            receita_model = dict(secao)['SecaoModel']

            secao_conteudos = session_local.execute(
                select(SecaoConteudoModel).
                where(SecaoConteudoModel.id_secao == receita_model.id)
            ).scalars().all()

            conteudos = []
            for secao_conteudo in secao_conteudos:
                conteudo = session_local.execute(select(ConteudoModel).where(ConteudoModel.id == secao_conteudo.id)).one()
                conteudos.append(dict(conteudo)['ConteudoModel'].item)

            receita_json['itens'].append({
                'secao' : receita_model.nome,
                'conteudo' : conteudos
            })

        return receita_json
