import streamlit as st
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# CONFIGURAÇÕES
# ==========================================

load_dotenv()

st.set_page_config(
    page_title="davIA | Inteligência Artificial",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = os.getenv("GROQ_API_KEY")
ARQUIVO_HISTORICO = "historico_davia.json"

if not API_KEY:
    st.error("Configure GROQ_API_KEY no arquivo .env")
    st.stop()

client = Groq(api_key=API_KEY)

# ==========================================
# ESTILO VISUAL
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #0b1020;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263247;
}

[data-testid="stSidebar"] h2 {
    color: #a78bfa;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #94a3b8;
    font-size: 15px;
}

[data-testid="stChatMessage"] {
    background: #151e32;
    border: 1px solid #263247;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 12px;
}

.stChatInput textarea {
    background: #151e32;
    color: white;
}

.stButton button {
    border-radius: 10px;
    border: 1px solid #384766;
    background: #1e293b;
    color: white;
    transition: 0.2s;
}

.stButton button:hover {
    background: #4338ca;
    border-color: #818cf8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HISTÓRICO PERMANENTE
# ==========================================

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados if isinstance(dados, dict) else {}
        except (json.JSONDecodeError, OSError):
            st.error("Não foi possível carregar o histórico.")
    return {}


def salvar_historico():
    arquivo_temp = ARQUIVO_HISTORICO + ".tmp"

    with open(arquivo_temp, "w", encoding="utf-8") as arquivo:
        json.dump(
            st.session_state.conversas,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    os.replace(arquivo_temp, ARQUIVO_HISTORICO)


def nova_conversa():
    identificador = str(uuid.uuid4())

    st.session_state.conversas[identificador] = {
        "titulo": "Nova conversa",
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "mensagens": [
            {
                "role": "assistant",
                "content": "Olá! Eu sou a davIA. Como posso ajudar você hoje?"
            }
        ]
    }

    st.session_state.conversa_atual = identificador
    salvar_historico()


if "conversas" not in st.session_state:
    st.session_state.conversas = carregar_historico()

if "conversa_atual" not in st.session_state:
    st.session_state.conversa_atual = None

if (
    st.session_state.conversa_atual not in st.session_state.conversas
):
    if st.session_state.conversas:
        st.session_state.conversa_atual = next(
            iter(st.session_state.conversas)
        )
    else:
        nova_conversa()

# ==========================================
# BARRA LATERAL
# ==========================================

with st.sidebar:

    st.markdown("## 🤖 davIA")
    st.caption("Seu assistente inteligente")

    st.divider()

    if st.button("＋ Nova conversa", use_container_width=True):
        nova_conversa()
        st.rerun()

    st.markdown("### 📚 Histórico")

    for identificador, conversa in reversed(
        list(st.session_state.conversas.items())
    ):

        titulo = conversa["titulo"]

        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(
                "💬 " + titulo[:25],
                key="abrir_" + identificador,
                use_container_width=True
            ):
                st.session_state.conversa_atual = identificador
                st.rerun()

        with col2:
            if st.button(
                "✕",
                key="excluir_" + identificador
            ):
                del st.session_state.conversas[identificador]

                if st.session_state.conversa_atual == identificador:
                    st.session_state.conversa_atual = None

                salvar_historico()
                st.rerun()

    st.divider()

    st.caption("davIA • Versão 2.0")
    st.caption("Inteligência artificial")

# ==========================================
# ÁREA PRINCIPAL
# ==========================================

conversa = st.session_state.conversas[
    st.session_state.conversa_atual
]

st.markdown(
    '<div class="main-title">davIA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Seu assistente pessoal de inteligência artificial</div>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# EXIBIR MENSAGENS
# ==========================================

for mensagem in conversa["mensagens"]:

    with st.chat_message(
        mensagem["role"],
        avatar="🤖" if mensagem["role"] == "assistant" else "👤"
    ):
        st.markdown(mensagem["content"])

# ==========================================
# CAMPO DE PERGUNTAS
# ==========================================

pergunta = st.chat_input(
    "Converse com a davIA..."
)

if pergunta:

    conversa["mensagens"].append({
        "role": "user",
        "content": pergunta
    })

    if conversa["titulo"] == "Nova conversa":
        conversa["titulo"] = pergunta[:35]

    salvar_historico()

    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)

    instrucoes = {
        "role": "system",
        "content": (
            "Você é a davIA, um assistente de inteligência artificial "
            "inteligente, educado, profissional e prestativo. "
            "Responda em português quando o usuário falar português."
        )
    }

    mensagens_api = [instrucoes]

    for mensagem in conversa["mensagens"]:
        mensagens_api.append({
            "role": mensagem["role"],
            "content": mensagem["content"]
        })

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("davIA está pensando..."):

            try:
                resultado = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=mensagens_api
                )

                resposta = (
                    resultado.choices[0].message.content
                    or "Não consegui gerar uma resposta."
                )

            except Exception:
                resposta = (
                    "Não consegui conectar à inteligência artificial. "
                    "Verifique sua conexão e tente novamente."
                )

            st.markdown(resposta)

    conversa["mensagens"].append({
        "role": "assistant",
        "content": resposta
    })

    salvar_historico()
    st.rerun()