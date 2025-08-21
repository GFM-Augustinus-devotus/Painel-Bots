from Data_Base.db import SessionLocal, Base, engine
from Data_Base.DialogoBots import DialogoBots
from sqlalchemy import inspect, select, func


Base.metadata.create_all(bind=engine)
insp = inspect(engine)
tabelas = insp.get_table_names()

with SessionLocal() as session:

    session.add(DialogoBots(
        nome        = "Quiabo-Frito" ,     
        introducao  = "Olá!👋 Seja bem-vindo! Quiabo Frito. Que bom saber que você quer fazer seu evento com a gente! 😊",
        pergunta1   = "Me conta rapidinho: Qual o tipo de evento que você quer realizar?\n\nDigite apenas o número da opção 📝\n\n1. Aniversário\n2. Casamento\n3. Corporativo\n4. Outro tipo de evento (amigos, celebração, etc)",
        pergunta2   = "Massa! Vamos organizar seu aniversário com estilo 💛\nResponda-me essas perguntinhas para gente te enviar um orçamento personaçizado\n\nQual a data e o horário do evento?",
        pergunta3   = "E para quantas pessoas será o seu aniversário?",
        pergunta4   = "Perfeito! Estamos verificando a disponibilidade nessa data e logo mais nosso time vai entrar em contato com você por aqui para finalizar a reserva.\n\nSe tiver alguma observação, pode alinhar com o atendente",
        pergunta5   = "Legal! Nós adorams receber eventos especiais ✨\nVou Precisar de algumas informações para montar tudo certinho\n\nQual seria o formato do evento? Digite o número da opção 📝:\n\n1. Casa fechada e exclusiva\n2. Apenas uma área reservada",
        pergunta6   = "Show!✨ Evento exclusivo, a casa inteira para vocês\n\nAgora me conta, quantas pessoas estarão presentes?",
        pergunta7   = "Qual vai ser a data e o horário do evento?",
        pergunta9   = "Agora sobre o Cardápio, qual dessas opções você prefere? Digite o número da opção 📝:\n\n1. Apenas petisco\n2. Entrada e prato principal e sobremesa",
        pergunta10  = "Em relação às bebidas o que você gostaria de incluir? Digite o número da opção 📝:\n\n1. Apenas Softs(Refrigerantes, água e sucos)\n2. Chopp e Softs\n3. Chopp, Softs e Cerveja\n4. Chopp, Softs, Cerveja e Drinks",
        pergunta11  = "Tranquilo! Opções refrescantes e sem álcool",
        pergunta12  = "Ótimo! Vamos preparar um cardápio completo que encanta do começa ao fim",   
        pergunta13  = "Chopp gelado e softs na medida!",
        pergunta14  = "Ceverjinha ta liberada também",
        pergunta15  = "A gente vai caprichar nos drinks para completar e experiência",
        pergunta17  = "Ótimo! 😄 Vamos reservar o melhor espaço do Quiabo Frito para você",
        pergunta18  = "Agora me conta, quantas pessoas estarão presentes?",
        pergunta19  = "Ótimo! Vamos preparar um cardápio completo que encanta do começa ao fim",
        pergunta20  = "Reiniciando informações ----> Qual o tipo de evento que você quer realizar?",
        pergunta21  = "Maravilha! 🥳😃 Com essas informações, nosso time vai preparar uma proposta exclusiva para vocês\n\nEm breve, um atendente irá entrar em contato\n\nSe tiver alguma observação, pode alinhar com o atendente",
        pergunta22  = "Valor Incorreto ❌ Digite novamente"
    ))

    session.commit()
