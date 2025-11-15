from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, client, google_oauth

app = FastAPI(
    title="DashFlow API",
    description="API para relatórios automatizados de marketing",
    version="0.1.0"
)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "DashFlow API está rodando! 🚀",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Importar routers
from app.routers import auth, client

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(client.router, prefix="/clients", tags=["Clientes"])

# Criar tabelas no banco
from app.database import engine, Base
from app.models import user, client as client_model

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(google_oauth.router, prefix="/auth/google", tags=["Google OAuth"])