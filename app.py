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
        st.write("O Manual Prático e o Portal SASOA tornam compreensível o rito de criação de uma Spin-off no IFPI, eliminando o jargão jurídico e a linguagem administrativa hermética?")
        q1 = st.select_slider("Classificação Q1:", options=[1, 2, 3, 4, 5], value=5, key="q1")

        # Q2
        st.markdown("**Q2. Segurança Jurídica & Dedicação Exclusiva (DE)**")
        st.write("Os instrumentos normativos apresentados (Termo TARD, diretrizes da Lei nº 10.973/04 e pareceres da AGU) conferem segurança funcional efetiva para o pesquisador atuar na SOA?")
        q2 = st.select_slider("Classificação Q2:", options=[1, 2, 3, 4, 5], value=5, key="q2")

        # Q3
        st.markdown("**Q3. Operacionalidade no SUAP**")
        st.write("A esteira estruturada em 4 fases e a indicação de autuação sob nível RESTRITO (LAI - Segredo Industrial) evitam a perda de novidade e previnem diligências/retrabalhos no SUAP?")
        q3 = st.select_slider("Classificação Q3:", options=[1, 2, 3, 4, 5], value=5, key="q3")

        # Q4
        st.markdown("**Q4. Apoio à Tomada de Decisão em Propriedade Intelectual (PI)**")
        st.write("O instrumental decisório (Scorecard Proteger vs. Publicar e rito INPI com hash SHA-256) é prático para orientar a melhor estratégia de proteção do ativo tecnológico?")
        q4 = st.select_slider("Classificação Q4:", options=[1, 2, 3, 4, 5], value=5, key="q4")

        # Q5
        st.markdown("**Q5. Governança de Royalties e Sustentabilidade**")
        st.write("O modelo de rateio financeiro via FAIFPI (1/3 inventores e 2/3 instituição) e as rotas de acompanhamento pós-contratual estão claros e aplicáveis à realidade do IFPI?")
        q5 = st.select_slider("Classificação Q5:", options=[1, 2, 3, 4, 5], value=5, key="q5")

        # Q6
        st.markdown("**Q6. Capacidade Resolutiva Global**")
        st.write("De modo geral, o ecossistema SASOA (Manual + Portal) é eficaz para converter pesquisas aplicadas desenvolvidas no IFPI em Spin-offs Acadêmicas estruturadas no mercado?")
        q6 = st.select_slider("Classificação Q6:", options=[1, 2, 3, 4, 5], value=5, key="q6")

        st.markdown("---")
        st.subheader("3. Parecer Qualitativo & Sugestões")
        comentarios = st.text_area(
            "Registre suas impressões qualitativas sobre os pontos fortes do produto ou sugestões para aprimoramento institucional:",
            placeholder="Exemplo: O manual facilitou a compreensão dos formulários necessários no SUAP e esclareceu as dúvidas quanto à Dedicação Exclusiva..."
        )

        submitted = st.form_submit_button("💾 Enviar Avaliação do PTT")
        if submitted:
            salvar_avaliacao(perfil, q1, q2, q3, q4, q5, q6, comentarios)
            st.success("✅ Avaliação registrada com sucesso! Os dados foram consolidados no banco de validação do PTT.")

# ==============================================================================
# ABA 2: PAINEL DE RESULTADOS (ESTATÍSTICA E TABELA)
# ==============================================================================
with tab_resultados:
    df_dados = carregar_dados()
    
    if df_dados.empty:
        st.info("ℹ️ Nenhuma avaliação registrada até o momento. Responda ao formulário na primeira aba para iniciar a consolidação.")
    else:
        st.subheader("📊 Métricas Consolidadas de Validação")
        
        col1, col2, col3 = st.columns(3)
        total_resp = len(df_dados)
        media_geral = df_dados[["q1_clareza", "q2_seguranca", "q3_suap", "q4_pi", "q5_royalties", "q6_global"]].mean().mean()
        
        # Cálculo de concordância (Notas 4 e 5)
        respostas_likert = df_dados[["q1_clareza", "q2_seguranca", "q3_suap", "q4_pi", "q5_royalties", "q6_global"]].values.flatten()
        concordancia_global = (sum(respostas_likert >= 4) / len(respostas_likert)) * 100

        with col1:
            st.metric("Total de Avaliações (N)", f"{total_resp}")
        with col2:
            st.metric("Média Geral do PTT (1 a 5)", f"{media_geral:.2f} / 5.00")
        with col3:
            st.metric("Índice de Concordância (IGC)", f"{concordancia_global:.1f}%")

        st.markdown("---")
        st.subheader("Médias por Dimensão Avaliada")
        
        medias = {
            "Q1. Desburocratização Cognitiva": df_dados["q1_clareza"].mean(),
            "Q2. Segurança Jurídica (DE)": df_dados["q2_seguranca"].mean(),
            "Q3. Operacionalidade no SUAP": df_dados["q3_suap"].mean(),
            "Q4. Tomada de Decisão em PI": df_dados["q4_pi"].mean(),
            "Q5. Governança de Royalties": df_dados["q5_royalties"].mean(),
            "Q6. Capacidade Resolutiva Global": df_dados["q6_global"].mean(),
        }
        
        df_medias = pd.DataFrame(list(medias.items()), columns=["Dimensão Avaliada", "Nota Média (1-5)"])
        st.bar_chart(df_medias.set_index("Dimensão Avaliada"))

        # Depoimentos Qualitativos Registrados
        st.markdown("---")
        st.subheader("Depoimentos Qualitativos Registrados")
        comentarios_validos = df_dados[df_dados["comentarios"].str.strip() != ""][["perfil", "comentarios", "data_hora"]]
        
        if comentarios_validos.empty:
            st.write("Nenhum comentário discursivo registrado.")
        else:
            for _, row in comentarios_validos.iterrows():
                st.markdown(f"""
                <div class='metric-box'>
                    <b>Perfil:</b> {row['perfil']} <br>
                    <b>Registro:</b> <small>{row['data_hora']}</small><br><br>
                    <i>"{row['comentarios']}"</i>
                </div>
                """, unsafe_allow_html=True)

        # Exportação dos dados para comprovação na dissertação
        st.markdown("---")
        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Dados Brutos (CSV) para a Dissertação",
            data=csv,
            file_name="dados_validacao_ptt_sasoa.csv",
            mime="text/csv"
        )
