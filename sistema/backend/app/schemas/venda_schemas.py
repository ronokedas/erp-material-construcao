"""
Schemas Pydantic - Vendas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class VendaItemCreate(BaseModel):
    produto_id: int
    quantidade: Decimal
    preco_unitario: Decimal
    desconto_item: Optional[Decimal] = 0


class VendaCreate(BaseModel):
    cliente_id: int
    tipo_pagamento: Optional[str] = None
    desconto: Optional[Decimal] = 0
    observacao: Optional[str] = None
    itens: List[VendaItemCreate]


class VendaItemResponse(BaseModel):
    id: int
    produto_id: Optional[int] = None
    quantidade: Decimal
    preco_unitario: Decimal
    desconto_item: Decimal
    subtotal_item: Decimal

    class Config:
        from_attributes = True


class VendaResponse(BaseModel):
    id: int
    cliente_id: Optional[int] = None
    numero_pedido: str
    data_venda: datetime
    tipo_pagamento: Optional[str] = None
    status: str
    subtotal: Decimal
    desconto: Decimal
    total: Decimal
    observacao: Optional[str] = None
    created_at: datetime
    itens: List[VendaItemResponse] = []

    class Config:
        from_attributes = True