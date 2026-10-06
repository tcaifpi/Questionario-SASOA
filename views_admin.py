import streamlit as st
from database import carregar_dados

def render_admin():
    if not st.session_state["admin_autenticado"]:
        st.title("🔐 Acesso Restrito ao NIT/IFPI")
        st.warning("Esta área é exclusiva para os administradores do ecossistema SASOA.")
        
        senha_digitada = st.text_input("Digite a senha de administrador:", type="password")
        
        if st.button("Entrar"):
            if senha_digitada == "sasoa2026": 
                st.session_state["admin_autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta. Acesso negado.")
    else:
        col_title, col_logout = st.columns([8, 2])
        with col_title:
            st.title("📊 Painel de Governança SASOA")
        with col_logout:
            if st.button("Sair / Logout", type="secondary"):
                st.session_state["admin_autenticado"] = False
                st.rerun()

        st.write("Visão geral dos autoenquadramentos registrados na base de dados (SQLite).")
        df_triagens = carregar_dados()

        if df_triagens.empty:
            st.warning("Nenhuma triagem registrada no banco de dados ainda.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total de Submissões", len(df_triagens))
            col2.metric("Elegíveis (Plena)", len(df_triagens[df_triagens['status_final'] == 'ELEGÍVEL (Habilitação Plena)']))
            col3.metric("Elegíveis (Condicionada)", len(df_triagens[df_triagens['status_final'] == 'ELEGÍVEL (Habilitação Condicionada)']))
            col4.metric("Inadequados/Retidos", len(df_triagens[df_triagens['status_final'].isin(['INADEQUADO PARA AUTUAÇÃO', 'RETENÇÃO NA BANCADA'])]))

            st.divider()
            st.subheader("Registros Detalhados")
            df_exibicao = df_triagens.rename(columns={
                "protocolo": "Protocolo", "data_hora": "Data/Hora",
                "admissibilidade": "Admissibilidade", "trl_stange": "Maturidade (TRL)",
                "estrategia_pi": "Estratégia de PI", "exclusividade": "Exclusividade",
                "status_final": "Status Final"
            })
            st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

            csv = df_triagens.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Baixar dados em CSV", data=csv, file_name='sasoa_triagens_export.csv', mime='text/csv')
