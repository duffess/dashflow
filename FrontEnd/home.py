import streamlit as st
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="DashFlow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API
API_URL = "http://localhost:8000"

# Inicializar session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

# Função de login
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

# Função de registro
def register(email, name, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"email": email, "name": name, "password": password}
        )
        if response.status_code == 201:
            return True, "Cadastro realizado! Faça login."
        else:
            error = response.json().get("detail", "Erro desconhecido")
            return False, error
    except Exception as e:
        return False, f"Erro ao conectar: {str(e)}"

# Função para pegar dados do usuário
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

# CSS customizado
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

# SIDEBAR - LOGIN/REGISTRO
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/FFFFFF?text=DashFlow", width=200)
    st.markdown("---")
    
    if st.session_state.token is None:
        # Tabs de Login e Registro
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
        
        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Entrar", use_container_width=True):
                if email and password:
                    with st.spinner("Entrando..."):
                        success, message = login(email, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Preencha todos os campos")
        
        with tab2:
            st.subheader("Cadastro")
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Nome", key="reg_name")
            reg_password = st.text_input("Senha", type="password", key="reg_password")
            
            if st.button("Criar conta", use_container_width=True):
                if reg_email and reg_name and reg_password:
                    with st.spinner("Criando conta..."):
                        success, message = register(reg_email, reg_name, reg_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("Preencha todos os campos")
    
    else:
        # Usuário logado
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

# CONTEÚDO PRINCIPAL
if st.session_state.token is None:
    # Landing page (não logado)
    st.markdown('<p class="big-font">📊 DashFlow</p>', unsafe_allow_html=True)
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
    
    # Buscar clientes
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        clients_response = requests.get(f"{API_URL}/clients/", headers=headers)
        num_clients = len(clients_response.json()) if clients_response.status_code == 200 else 0
    except:
        num_clients = 0
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Clientes", num_clients, "Cadastrados")
    
    with col2:
        st.metric("Campanhas", "0", "Adicione integrações")
    
    with col3:
        st.metric("Relatórios", "0", "Crie seu primeiro")
    
    with col4:
        st.metric("Gasto Total", "R$ 0,00", "Este mês")
    
    st.markdown("---")
    
    # Ações rápidas
    st.subheader("🚀 Ações Rápidas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("#### 📋 Gerenciar Clientes")
            st.markdown(f"Você tem **{num_clients} cliente(s)** cadastrado(s)")
            if st.button("Ver clientes", key="go_clients"):
                st.switch_page("pages/1_👥_Clientes.py")
    
    with col2:
        with st.container():
            st.markdown("#### 🔗 Conectar Integrações")
            st.markdown("Conecte suas contas de anúncios")
            if st.button("Configurar integrações", key="integrations"):
                st.info("🚧 Em desenvolvimento")
    
    st.markdown("---")
    
    # Próximos passos
    st.subheader("🎯 Próximos Passos")
    
    if num_clients == 0:
        st.info("👉 Comece adicionando seus clientes na página **Clientes**")
    else:
        st.success("✅ Você já tem clientes cadastrados!")
        st.info("👉 Próximo passo: Conectar Google Ads e Meta Ads (em breve)")
    
    # Info do usuário
    with st.expander("ℹ️ Informações da conta"):
        st.json(st.session_state.user)

# Footer
st.markdown("---")
st.caption("DashFlow v0.1.0 | Desenvolvido com ❤️ por Duffes")