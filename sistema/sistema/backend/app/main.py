"""
FastAPI - Application main entry point.
ERP Material de Construção
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, clientes, fornecedores, produtos, categorias, vendas, dashboard, orcamentos

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API do ERP para lojas de material de construção",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Desabilita redirect de trailing slash para não perder headers de auth
app.router.redirect_slashes = False

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(fornecedores.router, prefix="/api/fornecedores", tags=["Fornecedores"])
app.include_router(produtos.router, prefix="/api/produtos", tags=["Produtos"])
app.include_router(categorias.router, prefix="/api/categorias", tags=["Categorias"])
app.include_router(vendas.router, prefix="/api/vendas", tags=["Vendas"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(orcamentos.router, prefix="/api/orcamentos", tags=["Orçamentos"])


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}