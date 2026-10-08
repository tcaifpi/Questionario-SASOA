import streamlit as st
from database import salvar_feedback

def render_aba_publica():
    # Aviso metodológico de encerramento do lote da dissertação (Opção B)
    st.markdown("""
    <div style='background-color: #ecfdf5; border: 1px solid #a7f3d0; border-left: 5px solid #059669; border-radius: 6px; padding: 14px 18px; margin-bottom: 22px; font-size: 14px; color: #065f46; line-height: 1.5;'>
        <b>📌 MARCO METODOLÓGICO CONCLUÍDO:</b> A rodada formal de validação acadêmica do Produto Técnico-Tecnológico (PTT) 
        para fins da dissertação de mestrado (PROFNIT/IFPI) foi <b>encerrada com N = 18 avaliadores homologados e 95,3% de concordância global</b>.<br><br>
        O formulário abaixo permanece ativo para <b>contribuições contínuas e governança participativa</b>, subsidiando os ciclos de melhoria continuada do Manual Prático e do Portal SASOA.
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_feedback_ptt"):
        st.subheader("1. Perfil do Avaliador")
        perfil = st.selectbox(
            "Identifique sua atuação no ecossistema acadêmico/institucional:",
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
        st.write("Os instrumentos normativos apresentados (Termo TARD, diretrizes da Lei nº 10.973/04 e pareceres da AGU) conferem salvaguarda funcional efetiva para o pesquisador atuar na SOA?")
        q2 = st.select_slider("Classificação Q2:", options=[1, 2, 3, 4, 5], value=5, key="q2")

        # Q3
        st.markdown("**Q3. Operacionalidade no SUAP**")
        st.write("A esteira estruturada em 4 fases e a indicação mandatória de sigilo restrito (LAI) evitam perda de novidade e retrabalhos na instrução processual?")
        q3 = st.select_slider("Classificação Q3:", options=[1, 2, 3, 4, 5], value=5, key="q3")

        # Q4
        st.markdown("**Q4. Apoio à Tomada de Decisão em Propriedade Intelectual (PI)**")
        st.write("O instrumental decisório (Scorecard Proteger vs. Publicar e rito INPI/Blockchain com SHA-256) é prático para orientar a melhor estratégia de tutela do ativo?")
        q4 = st.select_slider("Classificação Q4:", options=[1, 2, 3, 4, 5], value=5, key="q4")

        # Q5
        st.markdown("**Q5. Governança de Royalties e Sustentabilidade**")
        st.write("O mecanismo de rateio via FAIFPI (1/3 inventores e 2/3 IFPI) e as rotas de acompanhamento pós-contratual são claros e aplicáveis à realidade do IFPI?")
        q5 = st.select_slider("Classificação Q5:", options=[1, 2, 3, 4, 5], value=5, key="q5")

        # Q6
        st.markdown("**Q6. Capacidade Resolutiva Global**")
        st.write("De modo geral, o ecossistema SASOA (Manual + Portal) é eficaz para converter pesquisas aplicadas desenvolvidas no IFPI em Spin-offs Acadêmicas estruturadas no mercado?")
        q6 = st.select_slider("Classificação Q6:", options=[1, 2, 3, 4, 5], value=5, key="q6")

        st.markdown("---")
        st.subheader("3. Parecer Qualitativo & Sugestões")
        comentarios = st.text_area(
            "Registre suas impressões sobre os pontos fortes ou sugestões de aprimoramento:",
            placeholder="Exemplo: As orientações sanaram as dúvidas sobre dedicação exclusiva e agilizaram a identificação dos formulários no SUAP..."
        )

        # Cláusula de Conformidade LGPD
        st.markdown("""
        <div style='background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px 16px; font-size: 13px; color: #475569; margin: 15px 0;'>
            🔒 <b>Conformidade com a LGPD (Lei nº 13.709/2018):</b><br>
            Este instrumento opera sob o princípio de <i>Privacy by Design</i>. A participação é totalmente anônima, 
            sem captação de dados pessoais identificáveis (nome, e-mail, CPF, matrícula) ou sensíveis. 
            Os dados destinam-se exclusivamente à avaliação técnica e melhoria continuada do PTT institucional.
        </div>
        """, unsafe_allow_html=True)

        enviado = st.form_submit_button("💾 Enviar Contribuição do PTT")
        if enviado:
            salvar_feedback(perfil, q1, q2, q3, q4, q5, q6, comentarios)
            st.success("✅ Contribuição registrada com sucesso! Ela integrará os relatórios de ciclo contínuo do SASOA.")
