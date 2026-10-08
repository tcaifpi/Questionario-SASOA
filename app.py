import streamlit as st
from database import init_db
from views_publico import render_aba_publica
from views_admin import render_aba_administrativa

# Configuração da Página
st.set_page_config(
    page_title="Avaliação do PTT — SASOA / IFPI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização Visual Institucional (Verde IFPI)
st.markdown("""
<style>
    .main-title {
        color: #1b4332;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .sub-title {
        color: #475569;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 18px;
    }
    .stButton>button {
        background-color: #1b4332;
        color: white;
        font-weight: 700;
        border-radius: 6px;
        padding: 10px 24px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2d6a4f;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados SQLite
init_db()

# Cabeçalho Principal
st.markdown("<div class='main-title'>🏛️ Instrumento de Avaliação da Eficácia do PTT — SASOA</div>", unsafe_allow_html=True)
st.markdown("""
<div class='sub-title'>
Este formulário integra a validação empírica do <b>Produto Técnico-Tecnológico (PTT)</b> desenvolvido no âmbito do PROFNIT/IFPI, 
composto pelo <b>Manual Prático de Governança (56 p.)</b> e pelo <b>Portal de Inovação SASOA</b>. 
Avalie em que medida as ferramentas apresentadas superam os entraves burocráticos e viabilizam as <i>Spin-offs</i> Acadêmicas no IFPI.
</div>
""", unsafe_allow_html=True)

# Abas de Navegação
tab_publica, tab_admin = st.tabs(["📝 Formulário de Avaliação do PTT", "🔒 Painel Restrito de Auditoria"])

with tab_publica:
    render_aba_publica()

with tab_admin:
    render_aba_administrativa()
