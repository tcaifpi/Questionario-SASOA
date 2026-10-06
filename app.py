
import streamlit as st
from database import init_db
from views_publico import render_publico
from views_admin import render_admin

# Inicializa o banco de dados SQLite
init_db()

# Gerenciamento de sessão para autenticação administrativa
if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Configuração da Página
st.set_page_config(page_title="SASOA | Governança", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #006400; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #004d00; color: white; }
    </style>
""", unsafe_allow_html=True)

# Menu Lateral
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Marca_Instituto_Federal_do_Piau%C3%AD.svg/1200px-Marca_Instituto_Federal_do_Piau%C3%AD.svg.png", width=150)
st.sidebar.title("Menu SASOA")
menu = st.sidebar.radio("Navegação:", ["📝 Nova Triagem (Público)", "🔐 Painel de Resultados (Admin)"])

# Roteamento das telas
if menu == "📝 Nova Triagem (Público)":
    render_publico()
elif menu == "🔐 Painel de Resultados (Admin)":
    render_admin()
