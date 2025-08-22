from sqlalchemy import Column, String, Integer, TIMESTAMP, text, func, quoted_name, ForeignKey
from .db import Base

class RespostaCliente():
    __tablename__ = "Resposta-Cliente"
    __tableargs__ = {"scheme": "public"}

    id         = Column(Integer, primary_key=True, autoincrement=True)
    bot_key    = Column(quoted_name("Chave Bot", True), Integer, foreign_key=True)
    cliente_key= Column(quoted_name("Chave Cliente", True), Integer, foreign_key=True)
    nome       = Column(quoted_name("Nome Cliente", True), String)
    inicio     = Column(quoted_name("Mensagem Incial", True), String)
    resposta1  = Column(quoted_name("Resposta 1", True), String)
    resposta2  = Column(quoted_name("Resposta 2", True), String)
    resposta3  = Column(quoted_name("Resposta 3", True), String)
    resposta4  = Column(quoted_name("Resposta 4", True), String)
    resposta5  = Column(quoted_name("Resposta 5", True), String)
    resposta6  = Column(quoted_name("Resposta 6", True), String)
    resposta7  = Column(quoted_name("Resposta 7", True), String)
    resposta8  = Column(quoted_name("Resposta 8", True), String)
    resposta9  = Column(quoted_name("Resposta 9", True), String)
    resposta10 = Column(quoted_name("Resposta 10", True), String)
    resposta11 = Column(quoted_name("Resposta 11", True), String)
    resposta12 = Column(quoted_name("Resposta 12", True), String)
    resposta13 = Column(quoted_name("Resposta 13", True), String)
    resposta14 = Column(quoted_name("Resposta 14", True), String)
    resposta15 = Column(quoted_name("Resposta 15", True), String)
    resposta16 = Column(quoted_name("Resposta 16", True), String)
    resposta17 = Column(quoted_name("Resposta 17", True), String)
    resposta18 = Column(quoted_name("Resposta 18", True), String)
    resposta19 = Column(quoted_name("Resposta 19", True), String)
    resposta20 = Column(quoted_name("Resposta 20", True), String)
    resposta21 = Column(quoted_name("Resposta 21", True), String)
    resposta22 = Column(quoted_name("Resposta 22", True), String)
    registrado_em = Column(quoted_name("Registrado Em", True), TIMESTAMP(timezone=True), server_default=text("(now() AT TIME ZONE 'America/Sao_Paulo'::text)"))