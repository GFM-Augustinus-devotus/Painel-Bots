# main.py
import streamlit as st
import pandas as pd
import re
from html import escape
from sqlalchemy import inspect, select, func
from pathlib import Path
from html import escape
from Data_Base.db import engine, SessionLocal, Base
from Data_Base.DraAnelise import DraAneliseAgendamento
from Data_Base.QuiaboFrito import QuiaboFrito
from Data_Base.DialogoBots import DialogoBots

# — Variáveis do tema vindas do config.toml —
PRIMARY = st.get_option("theme.primaryColor") or "#1DB954"
SURFACE  = st.get_option("theme.secondaryBackgroundColor") or "#181818"
TEXT     = st.get_option("theme.textColor") or "#FFFFFF"

# — Injeta as variáveis CSS no :root (cores do tema) —
st.markdown(
    f"""
    <style>
      :root {{
        --bubble-user-bg: {PRIMARY};
        --bubble-user-text: #FFFFFF;
        --bubble-bot-bg: {SURFACE};
        --bubble-bot-text: {TEXT};
        --bubble-shadow: 0 4px 14px rgba(0,0,0,.18);
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# — Carrega o arquivo externo de CSS —
def load_css(path: str):
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Arquivo CSS não encontrado: {path}")

load_css("assets/chat.css")


# cria as tabelas (se não existirem)
Base.metadata.create_all(bind=engine)
insp = inspect(engine)
tabelas = insp.get_table_names()

with SessionLocal() as session:
#Diálogos dos Bots

    has_any = session.execute(select(DialogoBots.id).limit(1)).first() is not None

    if not has_any:
        session.add(DialogoBots(
           nome = "Dra-Anelise-Agendamentos",
           introducao = "Olá!👋 Seja bem-vindo(a) ao consultório da Dra. Anelise Daher. 😊",
           pergunta1 = "Aqui é a Renata! Sou a assistente virtual da Dra. Anelise e estou aqui para facilitar o seu atendimento.",
           pergunta2 = "Qual o nome do paciente? 📋",
           pergunta3 = "Digite apenas o número da opção 📝",
           pergunta4 = """1. (0 a 2 anos) 2. (3 a 5 anos) 3. (6 a 10 anos) 4. (Mais de 10 anos)""",
           pergunta5 = "E você está buscando qual tipo de atendimento ",
           pergunta6 = """ 1. Primeira consulta 2. Avaliação geral 3. Limpeza e prevenção 4. Retorno 5. Urgência""",
           pergunta7 = "Para vocês o melhor período para agendarmos um horário com a Dra. Anelise? 👨‍⚕",
           pergunta8 = """1. Manhã (9h-12h) 2. Tarde (14h-17h) 3. Indiferente Pode me contatar quando disponível""",
           pergunta9 = "Entendido! ✅ Então vamos marcar a aconsulta do(a) Luiza !",
           pergunta10 = "Conte-me, você já é paciente da Dra. Anelise? 📌", 
           pergunta11 = " 1. Já sou paciente 2. Quero ser paciente",
           pergunta12 = "Entendi! 💬 É importante que você saiba que estará em boas mãos! A Dra Anelise é a Odontopediatra com mais experiência e Goiânia.📍"
        ))

        session.commit()

# Dra. Anelise

    usuario_col_dra = "nomeUsuario"

    totalDraAnelise = session.scalar(select(func.count(DraAneliseAgendamento.id)))

    todasRespostasDraAnelise = session.scalar(select(func.count()).select_from(DraAneliseAgendamento).where(DraAneliseAgendamento.etapas.in_([2, 4]))) or 0

    has_any = session.execute(select(DraAneliseAgendamento.id).limit(1)).first() is not None

    nomeUsuarioDraAnelise = session.scalars(select(DraAneliseAgendamento.nome_usuario)).all()

    nomeUsuarioDraAnelise = [n.strip() for n in nomeUsuarioDraAnelise if isinstance(n, str) and n.strip()]

    nomeUsuarioDraAnelise = list(dict.fromkeys(nomeUsuarioDraAnelise))

#Quiabo Frito

    usuario_col_qf = "Nome Usuário"

    totalQuiaboFrito = session.scalar(select(func.count(QuiaboFrito.id)))

    todasRespostasQuiaboFrito = session.scalar(select(func.count()).select_from(QuiaboFrito).where(QuiaboFrito.etapa == 10)) or 0

    has_any = session.execute(select(QuiaboFrito.id).limit(1)).first() is not None

    nomeUsuarioQuiaboFrito = session.scalars(select(QuiaboFrito.nome_usuario)).all()

    nomeUsuarioQuiaboFrito = [n.strip() for n in nomeUsuarioQuiaboFrito if isinstance(n, str) and n.strip()]

    nomeUsuarioQuiaboFrito = list(dict.fromkeys(nomeUsuarioQuiaboFrito))


#Diálogos entre o usuário 

# --- HELPER PARA EXIBIR TRECHO DE CONVERSA ---

def _first_col(dfx, *cands):
    for c in cands:
        if c in dfx.columns:
            return c
    return None

def mostrar_conversa(df: pd.DataFrame, usuario_col: str, usuario_val):
    """Renderiza a conversa em balões, com heurísticas para esquemas comuns de armazenamento."""
    sub = df.loc[df[usuario_col] == usuario_val].copy()
    if sub.empty:
        st.info("Nenhum registro para este usuário.")
        return

    # ---------- 1) Esquema 'longo': uma linha por mensagem ----------

    msg_col = _first_col(sub, "mensagem", "mensagens", "texto", "message", "conteudo", "content")
    who_col = _first_col(sub, "autor", "remetente", "from", "quem", "sender", "origem", "direcao", "role")
    ts_col  = _first_col(sub, "timestamp", "data_hora", "data", "hora", "created_at", "dt", "quando")

    def _role_from_author(a_raw: str) -> str:
        a = (a_raw or "").strip().lower()
        if a in {"user", "usuario", "cliente", "humano", "pessoa"}:
            return "user"
        if a in {"bot", "assistente", "sistema", "ai", "atendente", "robô", "robo", "renata"}:
            return "bot"
        # fallback: se há texto no autor, tratamos como user; vazio -> bot
        return "user" if a else "bot"

    def _emit_balloons(eventos):
        st.markdown('<div class="chat">', unsafe_allow_html=True)
        for role, msg, autor, ts in eventos:
            if not msg:
                continue
            autor_txt = autor or ("Usuário" if role == "user" else "Bot")
            ts_txt = ""
            if ts is not None and str(ts).strip():
                try:
                    if hasattr(ts, "strftime"):
                        ts_txt = ts.strftime("%d/%m/%Y %H:%M")
                    else:
                        ts_txt = str(ts)
                except Exception:
                    ts_txt = ""
            st.markdown(
                f"""
                <div class="chat-row {role}">
                  <div class="bubble {role}">
                    {escape(str(msg))}
                    <div class="meta">{escape(str(autor_txt))}{(' · ' + escape(str(ts_txt))) if ts_txt else ''}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Tenta ordenar por tempo se existir coluna temporal
    if ts_col is not None:
        try:
            sub[ts_col] = pd.to_datetime(sub[ts_col], errors="coerce")
            sub = sub.sort_values(ts_col, kind="stable")
        except Exception:
            pass

    if msg_col is not None:
        eventos = []
        for _, row in sub.iterrows():
            msg = row.get(msg_col)
            if pd.isna(msg) or str(msg).strip() == "":
                continue
            autor_raw = row.get(who_col) if who_col else ""
            role = _role_from_author(str(autor_raw))
            ts = row.get(ts_col) if ts_col else None
            eventos.append((role, str(msg), str(autor_raw) if autor_raw else None, ts))
        if eventos:
            _emit_balloons(eventos)
            return
        # se tinha msg_col, mas todas vazias, cai para os próximos modos

    # ---------- 2) Esquema 'largo' perguntaN/respostaN ----------
    # Procura colunas tipo pergunta1, pergunta_1, resposta1, resposta_1...
    cols = list(sub.columns)
    ptn_perg = re.compile(r"^pergunta[\s_\-]*([0-9]+)$", re.IGNORECASE)
    ptn_resp = re.compile(r"^resposta[\s_\-]*([0-9]+)$", re.IGNORECASE)

    perguntas = {}
    respostas = {}
    for c in cols:
        m = ptn_perg.match(str(c))
        if m:
            perguntas[int(m.group(1))] = c
        m = ptn_resp.match(str(c))
        if m:
            respostas[int(m.group(1))] = c

    if perguntas or respostas:
        # Considera a primeira linha do usuário (mais comum nesse esquema)
        row0 = sub.iloc[0]
        eventos = []
        for i in sorted(set(list(perguntas.keys()) + list(respostas.keys()))):
            c_perg = perguntas.get(i)
            c_resp = respostas.get(i)
            if c_perg and pd.notna(row0.get(c_perg)) and str(row0.get(c_perg)).strip():
                eventos.append(("bot", str(row0.get(c_perg)), "Bot", None))
            if c_resp and pd.notna(row0.get(c_resp)) and str(row0.get(c_resp)).strip():
                eventos.append(("user", str(row0.get(c_resp)), "Usuário", None))
        if eventos:
            _emit_balloons(eventos)
            return

    # ---------- 3) Esquema 'largos' por papel: mensagemBot*/mensagemUsuario* ----------
    # Ex.: mensagemBot, mensagemBot2, mensagemUsuario, mensagemUsuario2...
    def _collect_cols(prefix):
        rx = re.compile(rf"^{re.escape(prefix)}([0-9]*)$", re.IGNORECASE)
        found = []
        for c in cols:
            m = rx.match(str(c))
            if m:
                idx = int(m.group(1)) if m.group(1) else 1
                found.append((idx, c))
        return [c for _, c in sorted(found)]

    bot_cols = _collect_cols("mensagemBot") + _collect_cols("msgBot") + _collect_cols("bot")
    user_cols = _collect_cols("mensagemUsuario") + _collect_cols("msgUsuario") + _collect_cols("usuario")

    if bot_cols or user_cols:
        row0 = sub.iloc[0]
        # Intercala por índice quando possível
        max_len = max(len(bot_cols), len(user_cols))
        eventos = []
        for i in range(max_len):
            if i < len(bot_cols):
                val = row0.get(bot_cols[i])
                if pd.notna(val) and str(val).strip():
                    eventos.append(("bot", str(val), "Bot", None))
            if i < len(user_cols):
                val = row0.get(user_cols[i])
                if pd.notna(val) and str(val).strip():
                    eventos.append(("user", str(val), "Usuário", None))
        if eventos:
            _emit_balloons(eventos)
            return

    # ---------- 4) Fallback ----------
    st.info("Não encontrei coluna de mensagens neste formato. Mostrando os registros do usuário.")
    st.dataframe(sub)
    # (se quiser depurar, descomente:)
    # st.caption(f"Colunas: {list(sub.columns)}")

#---------------------------
# Front-End ----> Streamlit
#---------------------------

st.title("Painel de Análise dos Bots")
if "Dra-Anelise-Agendamentos" in tabelas:
    dfDraAnelise = pd.read_sql_table("Dra-Anelise-Agendamentos", con=engine) 
    st.write("""## Dra. Anelise""")
    st.write(f"""### Usuários em contato com o Bot: {totalDraAnelise}""")
    st.write(f"""### Usuários que responderam todas as perguntas: {todasRespostasDraAnelise}""")
    #st.write("""### Clientes Convertidos: """)
    usuarioDraAnelise = st.selectbox("Escolha um usuário", options=nomeUsuarioDraAnelise, index=None, placeholder="...")
    st.subheader("--------------------------------------------")
    #st.dataframe(dfDraAnelise)

    # --- ABAS para o usuário selecionado (Dra. Anelise) ---
if usuarioDraAnelise:  # usando a MESMA variável já existente no seu código
    # detectar nome da coluna do usuário
    usuario_col_dra = next((c for c in ["nomeUsuario", "nome_usuario", "nome usuário"] if c in dfDraAnelise.columns), None)
    if usuario_col_dra:
        aba_resumo_dra, aba_conversa_dra = st.tabs(["Resumo", "Conversa"])
        with aba_resumo_dra:
            st.dataframe(dfDraAnelise.loc[dfDraAnelise[usuario_col_dra] == usuarioDraAnelise])
        with aba_conversa_dra:
            mostrar_conversa(dfDraAnelise, usuario_col_dra, usuarioDraAnelise)
    else:
        st.warning("Coluna de usuário não encontrada nesta tabela (procure por 'nome_usuario' ou 'nome usuário').")


if "Quiabo-Frito" in tabelas:
    dfQuiaboFrito = pd.read_sql_table("Quiabo-Frito", con=engine)
    st.write("""## Quiabo Frito""")
    st.write(f"""### Usuários em contato com o Bot: {totalQuiaboFrito}""")
    st.write(f"""### Usuários que responderam todas as perguntas: {todasRespostasQuiaboFrito}""")
    #st.write("""### Clientes Convervetidos: """)
    usuarioQuiaboFrito = st.selectbox("Escolha um usuário", options=nomeUsuarioQuiaboFrito, index=None, placeholder="...")
    st.subheader("--------------------------------------------")
    #st.dataframe(dfQuiaboFrito)

# --- ABAS para o usuário selecionado (Quiabo Frito) ---
if usuarioQuiaboFrito:  # mesma variável já usada por você
    usuario_col_qf = next((c for c in ["nomeUsuario", "Nome Usuário", "nome_usuario", "nome usuário"] if c in dfQuiaboFrito.columns), None)
    if usuario_col_qf:
        aba_resumo_qf, aba_conversa_qf = st.tabs(["Resumo", "Conversa"])
        with aba_resumo_qf:
            st.dataframe(dfQuiaboFrito.loc[dfQuiaboFrito[usuario_col_qf] == usuarioQuiaboFrito])
        with aba_conversa_qf:
            mostrar_conversa(dfQuiaboFrito, usuario_col_qf, usuarioQuiaboFrito)
    else:
        st.warning("Coluna de usuário não encontrada nesta tabela (procure por 'nome_usuario' ou 'nome usuário').")
