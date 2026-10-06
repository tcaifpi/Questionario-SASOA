import streamlit as st
from datetime import datetime
import uuid
from database import salvar_triagem

def render_publico():
    st.title("🚀 SASOA: Autoenquadramento e Triagem")
    st.info("Este formulário avalia a viabilidade de enquadramento da sua proposta como Spin-off Acadêmica. **Nenhum dado pessoal sensível é armazenado** (LGPD).")

    # FASE 1
    st.header("Fase 1: Admissibilidade e Vínculo")
    q1 = st.radio("1. A equipe possui vínculo com o IFPI (servidor, discente ou egresso até 2 anos)?", ("Sim", "Não"), index=None)
    q2 = st.radio("2. A proposta tem origem comprovada em atividades do IFPI?", ("Sim", "Não"), index=None)
    q3 = st.radio("3. A proposta utiliza ativos intangíveis do IFPI?", ("Sim", "Não"), index=None)
    q4 = st.radio("4. Possui anuência preliminar da Direção-Geral do Campus?", ("Sim", "Não"), index=None)

    # FASE 2
    st.header("Fase 2: Nível de Prontidão Tecnológica")
    trl_options = {
        "1": "TRL/STRL 1-2: Princípios básicos ou formulação do conceito",
        "3": "TRL/STRL 3: Prova de conceito laboratorial ou código básico",
        "4": "TRL/STRL 4: Validação em ambiente de laboratório/arquitetura",
        "5": "TRL/STRL 5-6: Validação em ambiente simulado ou relevante",
        "7": "TRL/STRL 7-9: Validação em ambiente operacional ou mercado"
    }
    trl_selecionado = st.selectbox("Estágio de desenvolvimento:", ["Selecione..."] + list(trl_options.values()))

    # FASE 3
    st.header("Fase 3: Proteção da Propriedade Intelectual")
    pi_patente = st.checkbox("Produto Físico/Químico (Patente)")
    pi_software = st.checkbox("Código-fonte (Registro de Software)")
    pi_knowhow = st.checkbox("Segredo do negócio (Know-how / NDA)")

    # FASE 4
    st.header("Fase 4: Rota de Licenciamento")
    exclusividade = st.radio("Exigirá exclusividade comercial sobre a tecnologia?", ("Sim", "Não"), index=None)

    st.divider()

    if st.button("GERAR E SALVAR DIAGNÓSTICO"):
        if None in [q1, q2, q3, q4, exclusividade] or trl_selecionado == "Selecione...":
            st.warning("⚠️ Responda a todas as perguntas antes de gerar o diagnóstico.")
        else:
            admissibilidade = "Atendida" if all(resp == "Sim" for resp in [q1, q2, q3, q4]) else "Não Atendida"
            
            estrategias_pi = []
            if pi_patente: estrategias_pi.append("Patente")
            if pi_software: estrategias_pi.append("Software")
            if pi_knowhow: estrategias_pi.append("Know-how")
            estrategia_pi_str = ", ".join(estrategias_pi) if estrategias_pi else "Nenhuma (Risco)"

            if admissibilidade == "Não Atendida":
                status_final = "INADEQUADO PARA AUTUAÇÃO"
                st.error(f"### 🛑 Status: {status_final}")
            else:
                if trl_selecionado == trl_options["1"]:
                    status_final = "RETENÇÃO NA BANCADA"
                    st.error(f"### 🛑 Status: {status_final}")
                else:
                    if trl_selecionado in [trl_options["3"], trl_options["4"]]:
                        status_final = "ELEGÍVEL (Habilitação Condicionada)"
                    else:
                        status_final = "ELEGÍVEL (Habilitação Plena)"
                    st.success(f"### ✅ Status: {status_final}")

            protocolo = f"SASOA-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:6].upper()}"
            salvar_triagem(protocolo, admissibilidade, trl_selecionado[:12], estrategia_pi_str, exclusividade, status_final)
            
            st.info(f"💾 **O seu diagnóstico foi registrado. Anote o seu Protocolo:** `{protocolo}`")
