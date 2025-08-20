#Tabela para registrar os fluxos das perguntas de cada Bot

from sqlalchemy import Column, String, Integer, TIMESTAMP, text, quoted_name
from .db import Base

class DialogoBots(Base):
    __tablename__ = "Dialogo-Bots"
    __tableargs__ = {"schemne": "public"}

    id              = Column(Integer, primary_key=True, autoincrement=True)
    nome            = Column(quoted_name("Nome do Bot", True), String)
    introducao      = Column(quoted_name("Introdução", True), String)
    pergunta1       = Column(quoted_name("Pergunta 1", True), String)
    pergunta2       = Column(quoted_name("Pergunta 2", True), String)
    pergunta3       = Column(quoted_name("Pergunta 3", True), String)
    pergunta4       = Column(quoted_name("Pergunta 4", True), String)
    pergunta5       = Column(quoted_name("Pergunta 5", True), String)
    pergunta6       = Column(quoted_name("Pergunta 6", True), String)
    pergunta7       = Column(quoted_name("Pergunta 7", True), String)
    pergunta8       = Column(quoted_name("Pergunta 8", True), String)
    pergunta9       = Column(quoted_name("Pergunta 9", True), String)
    pergunta10      = Column(quoted_name("Pergunta 10", True), String)
    pergunta11      = Column(quoted_name("Pergunta 11", True), String)
    pergunta12      = Column(quoted_name("Pergunta 12", True), String)
    registrado_em   = Column(quoted_name("Registrado em", True) , TIMESTAMP(timezone=True), server_default=text("(now() AT TIME ZONE 'America/Sao_Paulo'::text)"))