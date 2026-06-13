"""
API - CRUD Categorias
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Categoria
from app.schemas.cadastro_schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse

router = APIRouter()

@router.get("", response_model=List[CategoriaResponse])
@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(Categoria).filter(Categoria.empresa_id == current_user.empresa_id).order_by(Categoria.nome).all()

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    c = db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.empresa_id == current_user.empresa_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return c

@router.post("", response_model=CategoriaResponse, status_code=201)
@router.post("/", response_model=CategoriaResponse, status_code=201)
def criar_categoria(data: CategoriaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    c = Categoria(**data.model_dump(), empresa_id=current_user.empresa_id)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, data: CategoriaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    c = db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.empresa_id == current_user.empresa_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(c, key, value)
    db.commit(); db.refresh(c)
    return c

@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    c = db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.empresa_id == current_user.empresa_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    c.ativo = False
    db.commit()