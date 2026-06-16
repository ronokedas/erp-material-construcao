"""
API - CRUD Clientes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Cliente
from app.schemas.cadastro_schemas import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter()


@router.get("", response_model=List[ClienteResponse])
@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    search: str = "",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos os clientes da empresa."""
    query = db.query(Cliente).filter(
        Cliente.empresa_id == current_user.empresa_id
    )
    if search:
        query = query.filter(
            Cliente.nome.ilike(f"%{search}%") |
            Cliente.cpf_cnpj.ilike(f"%{search}%") |
            Cliente.telefone.ilike(f"%{search}%")
        )
    return query.order_by(Cliente.nome).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtém um cliente pelo ID."""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.empresa_id == current_user.empresa_id
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("", response_model=ClienteResponse, status_code=201)
@router.post("/", response_model=ClienteResponse, status_code=201)
def criar_cliente(
    data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cria um novo cliente."""
    cliente = Cliente(**data.model_dump(), empresa_id=current_user.empresa_id)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza um cliente."""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.empresa_id == current_user.empresa_id
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=204)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Exclui um cliente (desativa)."""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.empresa_id == current_user.empresa_id
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente.ativo = False
    db.commit()