from sqlalchemy import Boolean, Column, Integer, String
from models.banco import base as Base


class ReceitaModel(Base):
    __tablename__ = 'receita'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=False)
