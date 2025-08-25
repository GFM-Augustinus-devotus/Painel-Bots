# InserirDados.py
from sqlalchemy import select, inspect
from Data_Base.db import SessionLocal, Base, engine
from Data_Base.DraAnelise import DraAneliseAgendamento
from Data_Base.RespostaClientes import RespostaCliente
# from Data_Base.DialogoBots import DialogoBots  # se precisar

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# Só para ver as tabelas existentes
insp = inspect(engine)
print("Tabelas:", insp.get_table_names(schema="public"))

with SessionLocal() as session:
    # Itera pelos objetos já carregando os campos direto
    for item in session.scalars(select(DraAneliseAgendamento)):
        # use diretamente os atributos do objeto
        rc = RespostaCliente(
            bot_key=1,
            cliente_key=item.id,
            nome=item.nome_usuario,
            inicio=item.nome_paciente,
            resposta1=str(item.idade_paciente) if item.idade_paciente is not None else None,
            resposta2=item.motivo_consulta,
            resposta3=item.hora_consulta,
            resposta4=item.conhece_dra,
            resposta5=item.etapas,
            resposta6=item.obs,
            # as demais ficam None por padrão
        )
        session.add(rc)

    session.commit()

    # Verifica se inseriu algo
    has_any = session.execute(select(RespostaCliente.id).limit(1)).first() is not None
    if has_any:
        print("Tabela RespostaCliente e dados inseridos corretamente, ver PgAdmin")
    else:
        print("Erro no processo")
