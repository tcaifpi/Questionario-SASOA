import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Avaliação do PTT — SASOA / IFPI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização visual institucional (Verde IFPI)
st.markdown("""
<style>
    .main-title {
        color: #1b4332;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .sub-title {
        color: #475569;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 20px;
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
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #1b4332;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# BANCO DE DADOS (SQLite)
# ==============================================================================
DB_NAME = "avaliacoes_sasoa.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            perfil TEXT,
            q1_clareza INTEGER,
            q2_seguranca INTEGER,
            q3_suap INTEGER,
            q4_pi INTEGER,
            q5_royalties INTEGER,
            q6_global INTEGER,
            comentarios TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_avaliacao(perfil, q1, q2, q3, q4, q5, q6, comentarios):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO avaliacoes (data_hora, perfil, q1_clareza, q2_seguranca, q3_suap, q4_pi, q5_royalties, q6_global, comentarios)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data_hora, perfil, q1, q2, q3, q4, q5, q6, comentarios))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM avaliacoes", conn)
    conn.close()
    return df

init_db()

# ==============================================================================
# CABEÇALHO DO FORMULÁRIO
# ==============================================================================
st.markdown("<div class='main-title'>🏛️ Instrumento de Avaliação da Eficácia do PTT — SASOA</div>", unsafe_allow_html=True)
st.markdown("""
<div class='sub-title'>
Este formulário integra a validação empírica do <b>Produto Técnico-Tecnológico (PTT)</b> desenvolvido no PROFNIT/IFPI, 
composto pelo <b>Manual Prático de Governança (56 p.)</b> e pelo <b>Portal de Inovação SASOA</b>. 
Avalie em que medida as ferramentas apresentadas são capazes de superar os entraves burocráticos e viabilizar a criação de <i>Spin-offs</i> Acadêmicas no IFPI.
</div>
""", unsafe_allow_html=True)

# Abas de Navegação: Formulário do Usuário e Painel de Resultados
tab_avaliacao, tab_resultados = st.tabs(["📝 Formulário de Avaliação do PTT", "📊 Painel de Resultados & Auditoria"])

# ==============================================================================
# ABA 1: FORMULÁRIO DE AVALIAÇÃO (LIKERT 1 A 5)
# ==============================================================================
with tab_avaliacao:
    with st.form("form_avaliacao_ptt"):
        st.subheader("1. Perfil do Avaliador")
        perfil = st.selectbox(
            "Selecione sua atuação principal no ecossistema acadêmico/institucional:",
            [
                "Docente Pesquisador do IFPI (Dedicação Exclusiva)",
                "Docente Pesquisador do IFPI (40h / 20h)",
                "Técnico-Administrativo em Educação (TAE) do IFPI",
                "Gestor / Membro de NIT / PROPI / Colegiado",
                "Discente / Egresso da Pós-Graduação (PROFNIT / Outros)",
                "Empreendedor / Parceiro Externo de Inovação"
            ]
        )

        st.markdown("---")
        st.subheader("2. Avaliação das Dimensões Resolutivas do PTT")
        st.caption("Escala: 1 = Discordo Totalmente | 2 = Discordo Parcialmente | 3 = Neutro | 4 = Concordo Parcialmente | 5 = Concordo Totalmente")

        # Q1
        st.markdown("**Q1. Desburocratização Cognitiva & Clareza**")
        st.write("O Manual Prático e o Portal SASOA tornam compreensível o rito de criação de uma Spin-off no IFPI, eliminando
