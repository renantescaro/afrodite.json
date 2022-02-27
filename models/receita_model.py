from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from models.banco import base as Base


class ReceitaModel(Base):
    __tablename__ = 'receita'

    id:int = Column(Integer, primary_key=True, index=True)
    nome:str = Column(String, unique=True, index=False)
