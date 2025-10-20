# código fast api app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DashFlow API",
    description="API para relatórios automatizados de marketing com IA",
    version="0.1.0"
)

# cors ( para o frontend )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # front local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "DashFlow API está rodando! Uhul!",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# importar routers aqui depois

from app.routers import auth

# incluir routers

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])

# tabela nos bancos

from app.database import engine, Base
from app.models import user # importa todos os models

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)