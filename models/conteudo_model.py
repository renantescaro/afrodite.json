from sqlalchemy import Boolean, Column, Integer, String
from models.banco import base as Base


class ConteudoModel(Base):
    __tablename__ = 'conteudo'

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, unique=False, index=False)
