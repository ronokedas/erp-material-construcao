"""
API - CRUD Produtos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Produto
from app.schemas.cadastro_schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter()

@router.get("", response_model=List[ProdutoResponse])
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(search: str = "", db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    query = db.query(Produto).filter(Produto.empresa_id == current_user.empresa_id)
    if search:
        query = query.filter(
            Produto.descricao.ilike(f"%{search}%") |
            Produto.codigo.ilike(f"%{search}%") |
            Produto.codigo_barras.ilike(f"%{search}%")
        )
    return query.order_by(Produto.descricao).all()

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == current_user.empresa_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return p

@router.post("", response_model=ProdutoResponse, status_code=201)
@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(data: ProdutoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    p = Produto(**data.model_dump(), empresa_id=current_user.empresa_id, estoque_atual=0)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, data: ProdutoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == current_user.empresa_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(p, key, value)
    db.commit(); db.refresh(p)
    return p

@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == produto_id, Produto.empresa_id == current_user.empresa_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    p.ativo = False
    db.commit()