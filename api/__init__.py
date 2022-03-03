from fastapi import FastAPI

app = FastAPI(title='Api Receitas')

from api.rotas import *