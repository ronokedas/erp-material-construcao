"""
API - CRUD Fornecedores
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Fornecedor
from app.schemas.cadastro_schemas import FornecedorCreate, FornecedorUpdate, FornecedorResponse

router = APIRouter()

@router.get("", response_model=List[FornecedorResponse])
@router.get("/", response_model=List[FornecedorResponse])
def listar_fornecedores(search: str = "", db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    query = db.query(Fornecedor).filter(Fornecedor.empresa_id == current_user.empresa_id)
    if search:
        query = query.filter(Fornecedor.nome.ilike(f"%{search}%") | Fornecedor.cpf_cnpj.ilike(f"%{search}%"))
    return query.order_by(Fornecedor.nome).all()

@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    f = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id, Fornecedor.empresa_id == current_user.empresa_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return f

@router.post("", response_model=FornecedorResponse, status_code=201)
@router.post("/", response_model=FornecedorResponse, status_code=201)
def criar_fornecedor(data: FornecedorCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    f = Fornecedor(**data.model_dump(), empresa_id=current_user.empresa_id)
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(fornecedor_id: int, data: FornecedorUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    f = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id, Fornecedor.empresa_id == current_user.empresa_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(f, key, value)
    db.commit(); db.refresh(f)
    return f

@router.delete("/{fornecedor_id}", status_code=204)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    f = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id, Fornecedor.empresa_id == current_user.empresa_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    f.ativo = False
    db.commit()