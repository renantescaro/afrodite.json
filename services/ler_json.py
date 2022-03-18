import json
from typing import Any, List
from entidades import Receita, Secao, Conteudo


class LerJson:
    def ler(self) -> List[Receita]:
        return self._montar_receitas()


    def _montar_conteudos(self, conteudos:Any) -> List[Conteudo]:
        conteudos_list = []
        for conteudo in conteudos:
            conteudo_obj = Conteudo(
                item=conteudo
            )
            conteudos_list.append(conteudo_obj)
        return conteudos_list


    def _montar_secoes(self, secoes:Any) -> List[Secao]:
        secoes_list = []
        for secao in secoes:
            # remove primeiro caracter se este for em branco
            secao_nome = secao['nome'][1:] if secao['nome'][0] == ' ' else secao['nome']

            conteudos_list = self._montar_conteudos(secao['conteudo'])
            secao_obj = Secao(
                nome=secao_nome,
                conteudo=conteudos_list
            )
            secoes_list.append(secao_obj)
        return secoes_list


    def _montar_receitas(self) -> List[Receita]:
        receitas_arquivo = open('static/afrodite.json', encoding='utf8')
        receitas = json.load(receitas_arquivo)

        receitas_list = []
        for receita in receitas:
            secoes_list = self._montar_secoes(receita['secao'])

            receita_obj = Receita(
                nome=receita['nome'],
                secao=secoes_list
            )
            receitas_list.append(receita_obj)
        return receitas_list
