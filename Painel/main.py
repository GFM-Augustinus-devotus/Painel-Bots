# main.py
import streamlit as st
import pandas as pd
import re
from html import escape
from sqlalchemy import inspect, select, func
from pathlib import Path
from Data_Base.db import engine, SessionLocal, Base
from Data_Base.DraAnelise import DraAneliseAgendamento
from Data_Base.QuiaboFrito import QuiaboFrito
from Data_Base.DialogoBots import DialogoBots

# cria as tabelas (se não existirem)
Base.metadata.create_all(bind=engine)
insp = inspect(engine)
tabelas = insp.get_table_names()

with SessionLocal() as session:

# Dra. Anelise

    usuario_col_dra = "nomeUsuario"

    totalDraAnelise = session.scalar(select(func.count(DraAneliseAgendamento.id)))

    todasRespostasDraAnelise = session.scalar(select(func.count()).select_from(DraAneliseAgendamento).where(DraAneliseAgendamento.etapas.in_([2, 4]))) or 0

    nomeUsuarioDraAnelise = session.scalars(select(DraAneliseAgendamento.nome_usuario)).all()

    nomeUsuarioDraAnelise = [n.strip() for n in nomeUsuarioDraAnelise if isinstance(n, str) and n.strip()]

    nomeUsuarioDraAnelise = list(dict.fromkeys(nomeUsuarioDraAnelise))

#Quiabo Frito

    usuario_col_qf = "Nome Usuário"

    totalQuiaboFrito = session.scalar(select(func.count(QuiaboFrito.id)))

    todasRespostasQuiaboFrito = session.scalar(select(func.count()).select_from(QuiaboFrito).where(QuiaboFrito.etapa == 10)) or 0

    nomeUsuarioQuiaboFrito = session.scalars(select(QuiaboFrito.nome_usuario)).all()

    nomeUsuarioQuiaboFrito = [n.strip() for n in nomeUsuarioQuiaboFrito if isinstance(n, str) and n.strip()]

    nomeUsuarioQuiaboFrito = list(dict.fromkeys(nomeUsuarioQuiaboFrito))


# — Carrega o arquivo externo de CSS —
def load_css(path: str):
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Arquivo CSS não encontrado: {path}")



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
                        ts_txt = ts.strftime("%d/%m/%Y %H:%M") #Retorna o horário da mensagem
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

#---------------------------
# Front-End ----> Streamlit
#---------------------------

st.title("Painel de Análise dos Bots")
load_css("assets/chat.css")
if "Dra-Anelise-Agendamentos" in tabelas:
    dfDraAnelise = pd.read_sql_table("Dra-Anelise-Agendamentos", con=engine) 
    st.write("""## Dra. Anelise""")
    st.write(f"""### Usuários em contato com o Bot: {totalDraAnelise}""")
    st.write(f"""### Usuários que responderam todas as perguntas: {todasRespostasDraAnelise}""")
    usuarioDraAnelise = st.selectbox("Escolha um usuário", options=nomeUsuarioDraAnelise, index=None, placeholder="...")

    # --- ABAS para o usuário selecionado (Dra. Anelise) ---
if usuarioDraAnelise:  
    usuario_col_dra = next((c for c in ["nomeUsuario", "nome_usuario", "nome usuário"] if c in dfDraAnelise.columns), None)
    if usuario_col_dra:
        aba_resumo_dra, aba_conversa_dra = st.tabs(["Resumo", "Conversa"])
        with aba_resumo_dra:
            st.dataframe(dfDraAnelise.loc[dfDraAnelise[usuario_col_dra] == usuarioDraAnelise])
        with aba_conversa_dra:
            if "Dialogo-Bots" in tabelas:
                dfDialogos = pd.read_sql_table("Dialogo-Bots", con=engine)

                ren = {"Nome do Bot": "nome_bot", "Introdução": "pergunta0", "Registrado em": "timestamp"}
                for n in range(1, 100):
                    col = f"Pergunta {n}"
                    if col in dfDialogos.columns:
                        ren[col] = f"pergunta{n}"
                dfDialogos = dfDialogos.rename(columns=ren)

                bot_alvo = "Dra-Anelise-Agendamentos"

                if bot_alvo in dfDialogos["nome_bot"].astype(str).unique():
                    mostrar_conversa(dfDialogos, "nome_bot", bot_alvo)
                else:
                    st.warning(f"Não encontrei registros para o bot {bot_alvo}.")
    else:
        st.warning("Coluna de usuário não encontrada nesta tabela (procure por 'nome_usuario' ou 'nome usuário').")

if "Quiabo-Frito" in tabelas:
    dfQuiaboFrito = pd.read_sql_table("Quiabo-Frito", con=engine)
    st.write("""## Quiabo Frito""")
    st.write(f"""### Usuários em contato com o Bot: {totalQuiaboFrito}""")
    st.write(f"""### Usuários que responderam todas as perguntas: {todasRespostasQuiaboFrito}""")
    usuarioQuiaboFrito = st.selectbox("Escolha um usuário", options=nomeUsuarioQuiaboFrito, index=None, placeholder="...")

# --- ABAS para o usuário selecionado (Quiabo Frito) ---
if usuarioQuiaboFrito:
    usuario_col_qf = next((c for c in ["nomeUsuario", "Nome Usuário", "nome_usuario", "nome usuário"] if c in dfQuiaboFrito.columns), None)
    if usuario_col_qf:
        aba_resumo_qf, aba_conversa_qf = st.tabs(["Resumo", "Conversa"])
        with aba_resumo_qf:
            st.dataframe(dfQuiaboFrito.loc[dfQuiaboFrito[usuario_col_qf] == usuarioQuiaboFrito])
        with aba_conversa_qf:
            if "Dialogo-Bots" in tabelas:
                dfDialogos = pd.read_sql_table("Dialogo-Bots", con=engine)

                ren = {"Nome do Bot": "nome_bot", "Introdução": "pergunta0", "Registrado em": "timestamp"}
                for n in range(1, 100):
                    col = f"Pergunta {n}"
                    if col in dfDialogos.columns:
                        ren[col] = f"pergunta{n}"
                dfDialogos = dfDialogos.rename(columns=ren)

                bot_alvo = "Quiabo-Frito"

                if bot_alvo in dfDialogos["nome_bot"].astype(str).unique():
                    mostrar_conversa(dfDialogos, "nome_bot", bot_alvo)
                else:
                    st.warning(f"Não encontrei registros para o bot {bot_alvo}.")
            
    else:
        st.warning("Coluna de usuário não encontrada nesta tabela (procure por 'nome_usuario' ou 'nome usuário').")
