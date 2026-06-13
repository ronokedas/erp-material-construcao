"""
API - Dashboard (métricas e indicadores)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.cadastro_models import Cliente, Produto, Fornecedor
from app.models.movimento_models import Venda
from app.core.dependencies import get_current_user
from app.models.auth_models import Usuario

router = APIRouter()


@router.get("")
@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Retorna métricas para o dashboard."""
    
    total_clientes = db.query(Cliente).filter(
        Cliente.empresa_id == current_user.empresa_id
    ).count()
    
    total_produtos = db.query(Produto).filter(
        Produto.empresa_id == current_user.empresa_id
    ).count()
    
    total_fornecedores = db.query(Fornecedor).filter(
        Fornecedor.empresa_id == current_user.empresa_id
    ).count()
    
    total_vendas = db.query(Venda).filter(
        Venda.empresa_id == current_user.empresa_id
    ).count()
    
    valor_total_vendas = db.query(func.coalesce(func.sum(Venda.total), 0)).filter(
        Venda.empresa_id == current_user.empresa_id
    ).scalar()
    
    vendas_hoje = db.query(Venda).filter(
        Venda.empresa_id == current_user.empresa_id,
        func.date(Venda.data_venda) == func.current_date()
    ).count()
    
    valor_vendas_hoje = db.query(func.coalesce(func.sum(Venda.total), 0)).filter(
        Venda.empresa_id == current_user.empresa_id,
        func.date(Venda.data_venda) == func.current_date()
    ).scalar()
    
    produtos_estoque_baixo = db.query(Produto).filter(
        Produto.empresa_id == current_user.empresa_id,
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()
    
    return {
        "total_clientes": total_clientes,
        "total_produtos": total_produtos,
        "total_fornecedores": total_fornecedores,
        "total_vendas": total_vendas,
        "valor_total_vendas": float(valor_total_vendas),
        "vendas_hoje": vendas_hoje,
        "valor_vendas_hoje": float(valor_vendas_hoje),
        "produtos_estoque_baixo": produtos_estoque_baixo,
    }