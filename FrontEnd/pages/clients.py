import streamlit as st
import requests
import pandas as pd

# Config
st.set_page_config(page_title="Clientes - DashFlow", page_icon="👥", layout="wide")

API_URL = "http://localhost:8000"

# Verificar se está logado
if 'token' not in st.session_state or st.session_state.token is None:
    st.warning("⚠️ Você precisa fazer login primeiro!")
    st.info("👈 Vá para a página inicial e faça login na barra lateral")
    st.stop()

# Headers de autenticação
headers = {"Authorization": f"Bearer {st.session_state.token}"}

# Funções de API
def create_client(name, email, phone, company):
    try:
        response = requests.post(
            f"{API_URL}/clients/",
            json={
                "name": name,
                "email": email if email else None,
                "phone": phone if phone else None,
                "company": company if company else None
            },
            headers=headers
        )
        if response.status_code == 201:
            return True, "Cliente criado com sucesso!"
        else:
            return False, response.json().get("detail", "Erro ao criar cliente")
    except Exception as e:
        return False, f"Erro ao conectar: {str(e)}"

def get_clients():
    try:
        response = requests.get(f"{API_URL}/clients/", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def delete_client(client_id):
    try:
        response = requests.delete(f"{API_URL}/clients/{client_id}", headers=headers)
        return response.status_code == 204
    except:
        return False

# Título
st.title("👥 Gerenciar Clientes")
st.markdown("---")

# Duas colunas: Formulário | Lista
col1, col2 = st.columns([1, 2])

# COLUNA 1: FORMULÁRIO DE CADASTRO
with col1:
    st.subheader("➕ Adicionar Novo Cliente")
    
    with st.form("client_form", clear_on_submit=True):
        name = st.text_input("Nome *", placeholder="Ex: Agência XYZ")
        email = st.text_input("Email", placeholder="contato@agencia.com")
        phone = st.text_input("Telefone", placeholder="(21) 99999-9999")
        company = st.text_input("Empresa", placeholder="XYZ Marketing Ltda")
        
        submitted = st.form_submit_button("✅ Adicionar Cliente", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("❌ O nome é obrigatório!")
            else:
                with st.spinner("Criando cliente..."):
                    success, message = create_client(name, email, phone, company)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    st.caption("* Campo obrigatório")

# COLUNA 2: LISTA DE CLIENTES
with col2:
    st.subheader("📋 Seus Clientes")
    
    # Botão de atualizar
    if st.button("🔄 Atualizar lista", key="refresh"):
        st.rerun()
    
    # Buscar clientes
    clients = get_clients()
    
    if not clients:
        st.info("📭 Você ainda não tem clientes cadastrados.\n\nAdicione seu primeiro cliente usando o formulário ao lado!")
    else:
        # Mostrar quantidade
        st.metric("Total de clientes", len(clients))
        
        st.markdown("---")
        
        # Exibir cada cliente em um card
        for client in clients:
            with st.container():
                col_info, col_actions = st.columns([4, 1])
                
                with col_info:
                    st.markdown(f"### {client['name']}")
                    
                    info_parts = []
                    if client.get('company'):
                        info_parts.append(f"🏢 {client['company']}")
                    if client.get('email'):
                        info_parts.append(f"📧 {client['email']}")
                    if client.get('phone'):
                        info_parts.append(f"📱 {client['phone']}")
                    
                    if info_parts:
                        st.markdown(" | ".join(info_parts))
                    
                    st.caption(f"ID: {client['id'][:8]}... | Criado em: {client['created_at'][:10]}")
                
                with col_actions:
                    if st.button("🗑️", key=f"delete_{client['id']}", help="Deletar cliente"):
                        if delete_client(client['id']):
                            st.success("Cliente deletado!")
                            st.rerun()
                        else:
                            st.error("Erro ao deletar")
                
                st.markdown("---")

# Estatísticas no final
st.markdown("### 📊 Estatísticas")
col1, col2, col3 = st.columns(3)

with col1:
    clients_with_email = len([c for c in clients if c.get('email')])
    st.metric("Com email", clients_with_email)

with col2:
    clients_with_phone = len([c for c in clients if c.get('phone')])
    st.metric("Com telefone", clients_with_phone)

with col3:
    clients_with_company = len([c for c in clients if c.get('company')])
    st.metric("Com empresa", clients_with_company)