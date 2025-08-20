from sqlalchemy import Column, String, Integer, TIMESTAMP, text, quoted_name
from .db import Base

class QuiaboFrito(Base):
    __tablename__= "Quiabo-Frito"
    __tableargs__ = {"schema": "public"}

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    registrado_em       = Column(quoted_name("Registrado em", True) , TIMESTAMP(timezone=True), server_default=text("(now() AT TIME ZONE 'America/Sao_Paulo'::text)"))
    usuario_id          = Column(quoted_name("UsuárioID", True), String)
    evento              = Column(quoted_name("Evento", True), String)
    quantidade_pessoas  = Column(quoted_name("Quantidade Pessoas", True), Integer)
    formato_evento      = Column(quoted_name("Formato Evento", True), String)
    cardapio            = Column(quoted_name("Cardápio", True), String)
    tipo_bebidas        = Column(quoted_name("Tipo Bebidas", True), String)
    etapa               = Column(quoted_name("Etapa", True), Integer, server_default=text("0"))
    nome_usuario        = Column(quoted_name("Nome Usuário", True), String)
    data_evento         = Column(quoted_name("Data Evento", True), String)
    mensagem            = Column(quoted_name("Mensagem", True),String)
