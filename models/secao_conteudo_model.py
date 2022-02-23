from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from models.banco import base as Base


class SecaoConteudoModel(Base):
    __tablename__ = 'secao_conteudo'

    id = Column(Integer, primary_key=True, index=True)
    id_secao = Column(Integer, ForeignKey('secao.id'))
    id_conteudo = Column(Integer, ForeignKey('conteudo.id'))
