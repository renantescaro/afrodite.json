from sqlalchemy import Boolean, Column, Integer, String
from models.banco import base as Base


class SecaoModel(Base):
    __tablename__ = 'secao'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, index=False)
