"""
Modelos SQLAlchemy - Cadastros (Clientes, Fornecedores, Produtos)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "cad_categorias"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    produtos = relationship("Produto", back_populates="categoria")


class Unidade(Base):
    __tablename__ = "cad_unidades"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(10), unique=True, nullable=False)
    nome = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    produtos = relationship("Produto", back_populates="unidade")


class Produto(Base):
    __tablename__ = "cad_produtos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    codigo = Column(String(50), nullable=False)
    codigo_barras = Column(String(50))
    descricao = Column(String(255), nullable=False)
    categoria_id = Column(Integer, ForeignKey("cad_categorias.id"))
    unidade_id = Column(Integer, ForeignKey("cad_unidades.id"))
    preco_custo = Column(DECIMAL(12, 2), default=0)
    preco_venda = Column(DECIMAL(12, 2), default=0)
    preco_prazo = Column(DECIMAL(12, 2), default=0)
    estoque_minimo = Column(DECIMAL(12, 3), default=0)
    estoque_atual = Column(DECIMAL(12, 3), default=0)
    ncm = Column(String(10))
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="produtos")
    unidade = relationship("Unidade", back_populates="produtos")


class Cliente(Base):
    __tablename__ = "cad_clientes"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    tipo_pessoa = Column(CHAR(1), default="F")
    cpf_cnpj = Column(String(18), unique=True)
    rg_ie = Column(String(20))
    telefone = Column(String(20))
    telefone2 = Column(String(20))
    email = Column(String(200))
    endereco = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(2))
    cep = Column(String(10))
    whatsapp = Column(String(20))
    limite_credito = Column(DECIMAL(12, 2), default=0)
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    vendas = relationship("Venda", back_populates="cliente")
    orcamentos = relationship("Orcamento", back_populates="cliente")


class Fornecedor(Base):
    __tablename__ = "cad_fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    tipo_pessoa = Column(CHAR(1), default="J")
    cpf_cnpj = Column(String(18), unique=True)
    ie = Column(String(20))
    telefone = Column(String(20))
    email = Column(String(200))
    endereco = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(2))
    cep = Column(String(10))
    contato_nome = Column(String(100))
    contato_telefone = Column(String(20))
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    compras = relationship("Compra", back_populates="fornecedor")