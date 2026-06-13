"""
Modelos SQLAlchemy - Movimentos (Vendas, Compras, Orçamentos, Estoque, Entregas)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Venda(Base):
    __tablename__ = "mov_vendas"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cad_clientes.id"))
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    numero_pedido = Column(String(20), unique=True, nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)
    tipo_pagamento = Column(String(30))
    status = Column(String(20), default="pendente")
    subtotal = Column(DECIMAL(12, 2), default=0)
    desconto = Column(DECIMAL(12, 2), default=0)
    total = Column(DECIMAL(12, 2), default=0)
    observacao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="vendas")
    itens = relationship("VendaItem", back_populates="venda", cascade="all, delete-orphan")


class VendaItem(Base):
    __tablename__ = "mov_vendas_itens"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("mov_vendas.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("cad_produtos.id"))
    quantidade = Column(DECIMAL(12, 3), nullable=False)
    preco_unitario = Column(DECIMAL(12, 2), nullable=False)
    desconto_item = Column(DECIMAL(12, 2), default=0)
    subtotal_item = Column(DECIMAL(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    venda = relationship("Venda", back_populates="itens")


class Compra(Base):
    __tablename__ = "mov_compras"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("cad_fornecedores.id"))
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    numero_pedido = Column(String(20), unique=True, nullable=False)
    data_compra = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pendente")
    subtotal = Column(DECIMAL(12, 2), default=0)
    desconto = Column(DECIMAL(12, 2), default=0)
    total = Column(DECIMAL(12, 2), default=0)
    observacao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    fornecedor = relationship("Fornecedor", back_populates="compras")
    itens = relationship("CompraItem", back_populates="compra", cascade="all, delete-orphan")


class CompraItem(Base):
    __tablename__ = "mov_compras_itens"

    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("mov_compras.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("cad_produtos.id"))
    quantidade = Column(DECIMAL(12, 3), nullable=False)
    preco_unitario = Column(DECIMAL(12, 2), nullable=False)
    desconto_item = Column(DECIMAL(12, 2), default=0)
    subtotal_item = Column(DECIMAL(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    compra = relationship("Compra", back_populates="itens")


class Orcamento(Base):
    __tablename__ = "mov_orcamentos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cad_clientes.id"))
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    numero_orcamento = Column(String(20), unique=True, nullable=False)
    data_orcamento = Column(DateTime, default=datetime.utcnow)
    data_validade = Column(Date)
    status = Column(String(20), default="ativo")
    subtotal = Column(DECIMAL(12, 2), default=0)
    desconto = Column(DECIMAL(12, 2), default=0)
    total = Column(DECIMAL(12, 2), default=0)
    observacao = Column(Text)
    venda_id = Column(Integer, ForeignKey("mov_vendas.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    itens = relationship("OrcamentoItem", back_populates="orcamento", cascade="all, delete-orphan")


class OrcamentoItem(Base):
    __tablename__ = "mov_orcamentos_itens"

    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer, ForeignKey("mov_orcamentos.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("cad_produtos.id"))
    quantidade = Column(DECIMAL(12, 3), nullable=False)
    preco_unitario = Column(DECIMAL(12, 2), nullable=False)
    desconto_item = Column(DECIMAL(12, 2), default=0)
    subtotal_item = Column(DECIMAL(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    orcamento = relationship("Orcamento", back_populates="itens")


class Estoque(Base):
    __tablename__ = "mov_estoque"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("cad_produtos.id"), nullable=False)
    tipo = Column(String(10), nullable=False)
    quantidade = Column(DECIMAL(12, 3), nullable=False)
    saldo_anterior = Column(DECIMAL(12, 3), default=0)
    saldo_atual = Column(DECIMAL(12, 3), default=0)
    documento_tipo = Column(String(30))
    documento_id = Column(Integer)
    observacao = Column(Text)
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Entrega(Base):
    __tablename__ = "mov_entregas"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    venda_id = Column(Integer, ForeignKey("mov_vendas.id"))
    cliente_id = Column(Integer, ForeignKey("cad_clientes.id"))
    endereco_entrega = Column(String(255))
    data_agendada = Column(Date)
    data_entrega = Column(DateTime)
    status = Column(String(20), default="pendente")
    observacao = Column(Text)
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)