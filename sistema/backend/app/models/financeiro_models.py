"""
Modelos SQLAlchemy - Financeiro (Contas, Caixa)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class CategoriaFinanceira(Base):
    __tablename__ = "fin_categorias"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(10), nullable=False)  # receita, despesa
    created_at = Column(DateTime, default=datetime.utcnow)


class ContaPagar(Base):
    __tablename__ = "fin_contas_pagar"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("cad_fornecedores.id"))
    categoria_id = Column(Integer, ForeignKey("fin_categorias.id"))
    descricao = Column(String(255), nullable=False)
    valor = Column(DECIMAL(12, 2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(DateTime)
    valor_pago = Column(DECIMAL(12, 2))
    status = Column(String(20), default="pendente")
    documento_tipo = Column(String(30))
    documento_id = Column(Integer)
    observacao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ContaReceber(Base):
    __tablename__ = "fin_contas_receber"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cad_clientes.id"))
    categoria_id = Column(Integer, ForeignKey("fin_categorias.id"))
    descricao = Column(String(255), nullable=False)
    valor = Column(DECIMAL(12, 2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_recebimento = Column(DateTime)
    valor_recebido = Column(DECIMAL(12, 2))
    status = Column(String(20), default="pendente")
    documento_tipo = Column(String(30))
    documento_id = Column(Integer)
    observacao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Caixa(Base):
    __tablename__ = "fin_caixa"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    tipo = Column(String(10), nullable=False)  # entrada, saida
    descricao = Column(String(255), nullable=False)
    valor = Column(DECIMAL(12, 2), nullable=False)
    data_movimento = Column(DateTime, default=datetime.utcnow)
    conta_pagar_id = Column(Integer, ForeignKey("fin_contas_pagar.id"))
    conta_receber_id = Column(Integer, ForeignKey("fin_contas_receber.id"))
    forma_pagamento = Column(String(30))
    observacao = Column(Text)
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    created_at = Column(DateTime, default=datetime.utcnow)