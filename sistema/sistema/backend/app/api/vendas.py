"""
API - CRUD Vendas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Produto
from app.models.movimento_models import Venda, VendaItem
from app.schemas.venda_schemas import VendaCreate, VendaResponse

router = APIRouter()


@router.get("", response_model=List[VendaResponse])
@router.get("/", response_model=List[VendaResponse])
def listar_vendas(
    search: str = "",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(Venda).filter(Venda.empresa_id == current_user.empresa_id)
    return query.order_by(Venda.created_at.desc()).limit(100).all()


@router.get("/{venda_id}", response_model=VendaResponse)
def obter_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    venda = db.query(Venda).filter(
        Venda.id == venda_id,
        Venda.empresa_id == current_user.empresa_id
    ).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


@router.post("", response_model=VendaResponse, status_code=201)
@router.post("/", response_model=VendaResponse, status_code=201)
def criar_venda(
    data: VendaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Gerar número do pedido
    count = db.query(Venda).filter(Venda.empresa_id == current_user.empresa_id).count()
    numero_pedido = f"V-{current_user.empresa_id:03d}-{count + 1:05d}"

    # Calcular totais
    subtotal = sum(
        item.quantidade * item.preco_unitario - item.desconto_item
        for item in data.itens
    )
    total = subtotal - data.desconto

    venda = Venda(
        empresa_id=current_user.empresa_id,
        cliente_id=data.cliente_id,
        usuario_id=current_user.id,
        numero_pedido=numero_pedido,
        tipo_pagamento=data.tipo_pagamento,
        status="confirmada",
        subtotal=subtotal,
        desconto=data.desconto or 0,
        total=total,
        observacao=data.observacao
    )
    db.add(venda)
    db.flush()

    # Criar itens
    for item_data in data.itens:
        item = VendaItem(
            venda_id=venda.id,
            produto_id=item_data.produto_id,
            quantidade=item_data.quantidade,
            preco_unitario=item_data.preco_unitario,
            desconto_item=item_data.desconto_item or 0,
            subtotal_item=item_data.quantidade * item_data.preco_unitario - (item_data.desconto_item or 0)
        )
        db.add(item)

        # Atualizar estoque
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
        if produto:
            produto.estoque_atual -= item_data.quantidade

    db.commit()
    db.refresh(venda)
    return venda


@router.delete("/{venda_id}", status_code=204)
def cancelar_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    venda = db.query(Venda).filter(
        Venda.id == venda_id,
        Venda.empresa_id == current_user.empresa_id
    ).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    venda.status = "cancelada"

    # Restaurar estoque
    for item in venda.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if produto:
            produto.estoque_atual += item.quantidade

    db.commit()