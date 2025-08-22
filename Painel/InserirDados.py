from sqlalchemy import select, inspect
from Data_Base.db import SessionLocal, Base, engine
from Data_Base.DraAnelise import DraAneliseAgendamento
from Data_Base.RespostaClientes import RespostaCliente
from Data_Base.DialogoBots import DialogoBots

#-------------------------------------

Base.metadata.create_all(bind=engine)
insp = inspect(engine)
tabelas = insp.get_table_names()

#-------------------------------------- Fazendo para a Dra. Anelise

with SessionLocal() as session:

    for item in session.scalars(select(DraAneliseAgendamento)):

        id_cliente = item.id
        nome_usuario = session.scalar(select(DraAneliseAgendamento.nome_usuario).where(DraAneliseAgendamento.id.in_([id_cliente])))
        nome_paciente = session.scalar(select(DraAneliseAgendamento.nome_paciente).where(DraAneliseAgendamento.id.in_([id_cliente])))
        idade_paciente = session.scalar(select(DraAneliseAgendamento.idade_paciente).where(DraAneliseAgendamento.id.in_([id_cliente])))
        motivo_consulta = session.scalar(select(DraAneliseAgendamento.motivo_consulta).where(DraAneliseAgendamento.id.in_([id_cliente])))
        hora_consulta = session.scalar(select(DraAneliseAgendamento.hora_consulta).where(DraAneliseAgendamento.id.in_([id_cliente])))
        conhece_dra = session.scalar(select(DraAneliseAgendamento.conhece_dra).where(DraAneliseAgendamento.id.in_([id_cliente])))
        etapas = session.scalar(select(DraAneliseAgendamento.etapas).where(DraAneliseAgendamento.id.in_([id_cliente])))
        obs = session.scalar(select(DraAneliseAgendamento.obs).where(DraAneliseAgendamento.id.in_([id_cliente])))

        print(f"Id: {id}\t | nome: {nome_usuario}")

        session.add(RespostaCliente(
        bot_key    = 1,
        cliente_key= id_cliente,
        nome       = nome_usuario,
        inicio     = nome_paciente,
        resposta1  = idade_paciente,
        resposta2  = motivo_consulta,
        resposta3  = hora_consulta,
        resposta4  = conhece_dra,
        resposta5  = etapas,
        resposta6  = obs,
        resposta7  = "",
        resposta8  = "",
        resposta9  = "",
        resposta10 = "",
        resposta11 = "",
        resposta12 = "",
        resposta13 = "",
        resposta14 = "",
        resposta15 = "",
        resposta16 = "",
        resposta17 = "",
        resposta18 = "",
        resposta19 = "",
        resposta20 = "",
        resposta21 = "",
        resposta22 = ""
        ))

        session.commit()

has_any = session.execute(select(RespostaCliente.id).limit(1)).first() is not None

if has_any:
    print("Tabela RespostaCliente e dados inseridos corretamente, ver PgAdmin")