"""
Schemas Pydantic - Orçamentos
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


class OrcamentoItemCreate(BaseModel):
    produto_id: int
    quantidade: Decimal
    preco_unitario: Decimal
    desconto_item: Optional[Decimal] = 0


class OrcamentoCreate(BaseModel):
    cliente_id: int
    data_validade: Optional[date] = None
    desconto: Optional[Decimal] = 0
    observacao: Optional[str] = None
    itens: List[OrcamentoItemCreate]


class OrcamentoItemResponse(BaseModel):
    id: int
    produto_id: Optional[int] = None
    quantidade: Decimal
    preco_unitario: Decimal
    desconto_item: Decimal
    subtotal_item: Decimal

    class Config:
        from_attributes = True


class OrcamentoResponse(BaseModel):
    id: int
    cliente_id: Optional[int] = None
    cliente_nome: Optional[str] = None
    usuario_id: Optional[int] = None
    usuario_nome: Optional[str] = None
    numero_orcamento: str
    data_orcamento: datetime
    data_validade: Optional[date] = None
    status: str
    subtotal: Decimal
    desconto: Decimal
    total: Decimal
    observacao: Optional[str] = None
    venda_id: Optional[int] = None
    created_at: datetime
    itens: List[OrcamentoItemResponse] = []

    class Config:
        from_attributes = True


class OrcamentoResumo(BaseModel):
    id: int
    cliente_nome: Optional[str] = None
    numero_orcamento: str
    data_orcamento: datetime
    data_validade: Optional[date] = None
    status: str
    total: Decimal
    venda_id: Optional[int] = None

    class Config:
        from_attributes = True