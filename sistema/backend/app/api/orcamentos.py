"""
API - CRUD Orçamentos + Converter para Venda + PDF
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, date, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario
from app.models.cadastro_models import Produto, Cliente
from app.models.movimento_models import Orcamento, OrcamentoItem, Venda, VendaItem
from app.models.sistema_models import Empresa
from app.schemas.orcamento_schemas import (
    OrcamentoCreate, OrcamentoResponse, OrcamentoResumo
)
from app.services.pdf_orcamento import gerar_pdf_orcamento

router = APIRouter()


@router.get("", response_model=List[OrcamentoResumo])
@router.get("/", response_model=List[OrcamentoResumo])
def listar_orcamentos(
    search: str = "",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = (
        db.query(Orcamento)
        .filter(Orcamento.empresa_id == current_user.empresa_id)
    )
    if search:
        query = query.join(Orcamento.cliente, isouter=True).filter(
            Cliente.nome.ilike(f"%{search}%")
        )

    orcamentos = query.order_by(Orcamento.created_at.desc()).limit(100).all()

    result = []
    for o in orcamentos:
        cliente_nome = None
        if o.cliente:
            cliente_nome = o.cliente.nome
        result.append(OrcamentoResumo(
            id=o.id,
            cliente_nome=cliente_nome,
            numero_orcamento=o.numero_orcamento,
            data_orcamento=o.data_orcamento,
            data_validade=o.data_validade,
            status=o.status,
            total=o.total,
            venda_id=o.venda_id,
        ))
    return result


@router.get("/{orcamento_id}", response_model=OrcamentoResponse)
def obter_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    orcamento = (
        db.query(Orcamento)
        .filter(
            Orcamento.id == orcamento_id,
            Orcamento.empresa_id == current_user.empresa_id
        )
        .options(
            joinedload(Orcamento.itens),
            joinedload(Orcamento.cliente),
        )
        .first()
    )
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")

    cliente_nome = orcamento.cliente.nome if orcamento.cliente else None
    usuario_nome = current_user.nome

    return OrcamentoResponse(
        id=orcamento.id,
        cliente_id=orcamento.cliente_id,
        cliente_nome=cliente_nome,
        usuario_id=orcamento.usuario_id,
        usuario_nome=usuario_nome,
        numero_orcamento=orcamento.numero_orcamento,
        data_orcamento=orcamento.data_orcamento,
        data_validade=orcamento.data_validade,
        status=orcamento.status,
        subtotal=orcamento.subtotal,
        desconto=orcamento.desconto,
        total=orcamento.total,
        observacao=orcamento.observacao,
        venda_id=orcamento.venda_id,
        created_at=orcamento.created_at,
        itens=[
            {
                "id": i.id,
                "produto_id": i.produto_id,
                "quantidade": i.quantidade,
                "preco_unitario": i.preco_unitario,
                "desconto_item": i.desconto_item,
                "subtotal_item": i.subtotal_item,
            }
            for i in orcamento.itens
        ],
    )


@router.post("", response_model=OrcamentoResponse, status_code=201)
@router.post("/", response_model=OrcamentoResponse, status_code=201)
def criar_orcamento(
    data: OrcamentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Validar cliente
    cliente = db.query(Cliente).filter(
        Cliente.id == data.cliente_id,
        Cliente.empresa_id == current_user.empresa_id
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Gerar número do orçamento
    count = db.query(Orcamento).filter(
        Orcamento.empresa_id == current_user.empresa_id
    ).count()
    numero_orcamento = f"ORC-{current_user.empresa_id:03d}-{count + 1:05d}"

    # Calcular totais
    subtotal = sum(
        item.quantidade * item.preco_unitario - item.desconto_item
        for item in data.itens
    )
    total = subtotal - data.desconto

    # Data de validade padrão: 30 dias
    data_validade = data.data_validade or (date.today() + timedelta(days=30))

    orcamento = Orcamento(
        empresa_id=current_user.empresa_id,
        cliente_id=data.cliente_id,
        usuario_id=current_user.id,
        numero_orcamento=numero_orcamento,
        data_validade=data_validade,
        subtotal=subtotal,
        desconto=data.desconto or 0,
        total=total,
        observacao=data.observacao,
    )
    db.add(orcamento)
    db.flush()

    # Criar itens
    for item_data in data.itens:
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
        item = OrcamentoItem(
            orcamento_id=orcamento.id,
            produto_id=item_data.produto_id,
            quantidade=item_data.quantidade,
            preco_unitario=item_data.preco_unitario,
            desconto_item=item_data.desconto_item or 0,
            subtotal_item=item_data.quantidade * item_data.preco_unitario - (item_data.desconto_item or 0),
        )
        db.add(item)

    db.commit()
    db.refresh(orcamento)

    return obter_orcamento(orcamento.id, db, current_user)


@router.delete("/{orcamento_id}", status_code=204)
def cancelar_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    orcamento = db.query(Orcamento).filter(
        Orcamento.id == orcamento_id,
        Orcamento.empresa_id == current_user.empresa_id
    ).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")

    if orcamento.status == "convertido":
        raise HTTPException(status_code=400, detail="Orçamento já convertido em venda não pode ser cancelado")

    orcamento.status = "cancelado"
    db.commit()


@router.post("/{orcamento_id}/converter", response_model=dict)
def converter_orcamento_em_venda(
    orcamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    orcamento = (
        db.query(Orcamento)
        .filter(
            Orcamento.id == orcamento_id,
            Orcamento.empresa_id == current_user.empresa_id
        )
        .options(joinedload(Orcamento.itens))
        .first()
    )
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")

    if orcamento.status == "convertido":
        raise HTTPException(status_code=400, detail="Orçamento já foi convertido em venda")

    if orcamento.status == "cancelado":
        raise HTTPException(status_code=400, detail="Orçamento cancelado não pode ser convertido")

    # Gerar número do pedido
    count = db.query(Venda).filter(Venda.empresa_id == current_user.empresa_id).count()
    numero_pedido = f"V-{current_user.empresa_id:03d}-{count + 1:05d}"

    # Criar venda
    venda = Venda(
        empresa_id=current_user.empresa_id,
        cliente_id=orcamento.cliente_id,
        usuario_id=current_user.id,
        numero_pedido=numero_pedido,
        subtotal=orcamento.subtotal,
        desconto=orcamento.desconto,
        total=orcamento.total,
        observacao=f"Convertido do orçamento {orcamento.numero_orcamento}. {orcamento.observacao or ''}",
    )
    db.add(venda)
    db.flush()

    # Criar itens da venda
    for item_orc in orcamento.itens:
        item_venda = VendaItem(
            venda_id=venda.id,
            produto_id=item_orc.produto_id,
            quantidade=item_orc.quantidade,
            preco_unitario=item_orc.preco_unitario,
            desconto_item=item_orc.desconto_item,
            subtotal_item=item_orc.subtotal_item,
        )
        db.add(item_venda)

        # Atualizar estoque
        produto = db.query(Produto).filter(Produto.id == item_orc.produto_id).first()
        if produto:
            produto.estoque_atual -= item_orc.quantidade

    # Atualizar status do orçamento
    orcamento.status = "convertido"
    orcamento.venda_id = venda.id

    db.commit()
    db.refresh(venda)

    return {
        "mensagem": "Orçamento convertido em venda com sucesso",
        "venda_id": venda.id,
        "numero_pedido": venda.numero_pedido,
    }


@router.get("/{orcamento_id}/pdf")
def download_pdf_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    orcamento = (
        db.query(Orcamento)
        .filter(
            Orcamento.id == orcamento_id,
            Orcamento.empresa_id == current_user.empresa_id
        )
        .options(
            joinedload(Orcamento.itens),
            joinedload(Orcamento.cliente),
        )
        .first()
    )
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")

    empresa = db.query(Empresa).filter(Empresa.id == current_user.empresa_id).first()

    pdf_bytes = gerar_pdf_orcamento(orcamento, empresa, current_user)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="orcamento_{orcamento.numero_orcamento}.pdf"'
        }
    )