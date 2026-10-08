import streamlit as st
import pandas as pd
from database import carregar_dados

SENHA_ADMIN = "sasoa2026"

def render_aba_administrativa():
    st.subheader("🔐 Acesso Restrito à Gestão da Pesquisa")
    senha = st.text_input("Introduza a palavra-passe de administração para visualizar as métricas:", type="password")

    if senha == "":
        st.info("ℹ️ Introduza a palavra-passe para auditar os dados da pesquisa e gerenciar as avaliações.")
        return

    if senha != SENHA_ADMIN:
        st.error("❌ Palavra-passe incorreta. Acesso negado.")
        return

    st.success("🔓 Acesso autorizado aos relatórios de validação.")
    st.markdown("---")

    # 1. CORTE HOMOLOGADO DA DISSERTAÇÃO (N = 18)
    st.subheader("📌 1. Lote Homologado da Dissertação (Corte Oficial N = 18)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avaliadores Homologados", "18 participantes")
    with col2:
        st.metric("Média Geral do PTT", "4.80 / 5.00")
    with col3:
        st.metric("Índice de Concordância (IGC)", "95.3%")

    df_oficial = pd.DataFrame({
        "Item / Dimensão Avaliada": [
            "Q1. Desburocratização Cognitiva & Clareza",
            "Q2. Segurança Jurídica & Dedicação Exclusiva (DE)",
            "Q3. Operacionalidade no SUAP",
            "Q4. Apoio à Tomada de Decisão em PI",
            "Q5. Governança de Royalties e Sustentabilidade",
            "Q6. Capacidade Resolutiva Global"
        ],
        "Média (1-5)": [4.89, 4.78, 4.83, 4.67, 4.72, 4.89],
        "Desvio Padrão (σ)": [0.32, 0.42, 0.38, 0.48, 0.46, 0.32],
        "% Concordância (4 e 5)": ["100.0%", "94.4%", "100.0%", "88.9%", "94.4%", "100.0%"],
        "Classificação": ["Excelente", "Excelente", "Excelente", "Muito Bom", "Excelente", "Excelente"]
    })
    st.dataframe(df_oficial, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2. NOVOS REGISTROS COLETADOS EM PRODUÇÃO
    st.subheader("📈 2. Registros Pós-Depósito (Feedback Contínuo)")
    df_dados = carregar_dados()

    if df_dados.empty:
        st.info("Nenhuma nova contribuição pós-depósito registrada até o momento.")
    else:
        st.write(f"Total de contribuições adicionais recebidas: **{len(df_dados)}**")
        st.dataframe(df_dados[["data_hora", "perfil", "q1_clareza", "q2_seguranca", "q3_suap", "q4_pi", "q5_royalties", "q6_global", "comentarios"]], use_container_width=True)

        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Dados Brutos Pós-Depósito (CSV)",
            data=csv,
            file_name="feedback_continuo_sasoa.csv",
            mime="text/csv"
        )
