# models.py
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, quoted_name
from .db import Base

class DraAneliseAgendamento(Base):
    __tablename__ = "Dra-Anelise-Agendamentos"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    registrado_em    = Column(quoted_name("Registrado em", True), TIMESTAMP(timezone=True), server_default=text("(now() AT TIME ZONE 'America/Sao_Paulo'::text)"))
    usuario_id       = Column(quoted_name("UsuárioID", True),String)
    nome_paciente    = Column(quoted_name("Nome Paciente", True),String)
    idade_paciente   = Column(quoted_name("Idade Paciente", True),String)
    motivo_consulta  = Column(quoted_name("Motivo Consulta", True), String)
    hora_consulta    = Column(quoted_name("Hora Consulta", True), String)
    conhece_dra      = Column(quoted_name("Conhece Dra", True), String)
    etapas           = Column(quoted_name("Etapas", True), Integer, server_default=text("0"))
    obs              = Column(quoted_name("Obs", True), String)
    nome_usuario     = Column(quoted_name("nomeUsuario", True), String)
