from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from models.banco import base as Base


class ReceitaSecaoModel(Base):
    __tablename__ = 'receita_secao'

    id = Column(Integer, primary_key=True, index=True)
    id_receita = Column(Integer, ForeignKey('receita.id'))
    id_secao = Column(Integer, ForeignKey('secao.id'))
