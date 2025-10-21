import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Home - DashFlow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

# função login

def login(email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            return True, "Login realizado com sucesso!"
        else:
            return False, "Email ou senha incorretos"
    except Exception as e:
        return False, f"Erro ao conectar: {str(e)}"
    
# função de registro

def register(email, name, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"email": email, "name": name, "password": password}
        )
        if response.status_code == 201:
            return True, "Cadastro realizado! Faça seu login."
        else:
            error = response.json().get("detail", "Erro desconhecido")
            return False, error
    except Exception as e:
        return False, f"Erro ao conectar: {str(e)}"
    
def get_user_data(token):
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None
    
st.markdown("""
    <style>
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# sidebar login/register

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/FFFFFF?text=DashFlow", width=200)
    st.markdown("---")

    if st.session_state.token is None:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])

        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                if email and password:
                    with st.spinner("Entrando..."):
                        sucess, message = login(email, password)
                        if sucess:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Por favor, preencha todos os campos.")
                    
        with tab2:
            st.subheader("Cadastro")
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Nome", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            if st.button("Cadastrar", use_container_width=True):
                if reg_email and reg_name and reg_password:
                    with st.spinner("Criando conta..."):
                        success, message = register(reg_email, reg_name, reg_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("Por favor, preencha todos os campos!")

    else:
        #usuario logado
        if st.session_state.user is None:
            st.session_state.user = get_user_data(st.session_state.token)
        if st.session_state.user:
            st.success("✅ Logado")
            st.write(f"**{st.session_state.user['name']}**")
            st.caption(st.session_state.user['email'])

            st.markdown("---")

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.token = None
                st.session_state.user = None
                st.rerun()

if st.session_state.token is None:
    #landingpage nao logada
    st.markdown('<p class="big-font"> 📊 DashFlow </p>', unsafe_allow_html=True)
    st.markdown("### Relatórios automatizados de marketing digital com IA")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**🔗 Integrações**\n\nGoogle Ads e Meta Ads em um só lugar")
    
    with col2:
        st.success("**🤖 IA Integrada**\n\nInsights automáticos sobre suas campanhas")
    
    with col3:
        st.warning("**📄 Relatórios PDF**\n\nDocumentos prontos para seus clientes")
    
    st.markdown("---")
    st.markdown("### Como funciona?")
    st.markdown("""
    1. **Conecte suas contas** de Google Ads e Meta Ads
    2. **Adicione seus clientes** e campanhas
    3. **Receba relatórios automáticos** com insights de IA
    4. **Compartilhe** com seus clientes em PDF
    """)
    
    st.info("👈 Faça login ou cadastre-se na barra lateral para começar!")

else:
    # Dashboard (logado)
    st.title(f"Bem-vindo, {st.session_state.user['name']}! 👋")
    
    # Métricas placeholder
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Clientes", "0", "Nenhum ainda")
    
    with col2:
        st.metric("Campanhas", "0", "Adicione integrações")
    
    with col3:
        st.metric("Relatórios", "0", "Crie seu primeiro")
    
    with col4:
        st.metric("Gasto Total", "R$ 0,00", "Este mês")
    
    st.markdown("---")
    
    # Próximos passos
    st.subheader("🚀 Próximos passos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("#### 1. Conectar Google Ads")
            st.markdown("Conecte sua conta do Google Ads para importar campanhas")
            if st.button("Conectar Google Ads", key="google_ads"):
                st.info("🚧 Em desenvolvimento")
    
    with col2:
        with st.container():
            st.markdown("#### 2. Conectar Meta Ads")
            st.markdown("Conecte sua conta do Meta (Facebook/Instagram)")
            if st.button("Conectar Meta Ads", key="meta_ads"):
                st.info("🚧 Em desenvolvimento")
    
    st.markdown("---")
    
    # Info do usuário
    with st.expander("ℹ️ Informações da conta"):
        st.json(st.session_state.user)

# Footer
st.markdown("---")
st.caption("DashFlow v0.1.0 | Desenvolvido com ❤️ por Duffes")