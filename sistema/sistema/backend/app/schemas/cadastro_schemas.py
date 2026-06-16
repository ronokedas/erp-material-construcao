"""
Schemas Pydantic - Cadastros
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


# ==================== CATEGORIAS ====================
class CategoriaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class CategoriaResponse(BaseModel):
    id: int
    empresa_id: int
    nome: str
    descricao: Optional[str] = None
    ativo: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ==================== PRODUTOS ====================
class ProdutoCreate(BaseModel):
    codigo: str
    codigo_barras: Optional[str] = None
    descricao: str
    categoria_id: Optional[int] = None
    unidade_id: Optional[int] = None
    preco_custo: Optional[Decimal] = 0
    preco_venda: Optional[Decimal] = 0
    preco_prazo: Optional[Decimal] = 0
    estoque_minimo: Optional[Decimal] = 0
    ncm: Optional[str] = None

class ProdutoUpdate(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    categoria_id: Optional[int] = None
    unidade_id: Optional[int] = None
    preco_custo: Optional[Decimal] = None
    preco_venda: Optional[Decimal] = None
    preco_prazo: Optional[Decimal] = None
    estoque_minimo: Optional[Decimal] = None
    ativo: Optional[bool] = None

class ProdutoResponse(BaseModel):
    id: int
    empresa_id: int
    codigo: str
    descricao: str
    codigo_barras: Optional[str] = None
    categoria_id: Optional[int] = None
    unidade_id: Optional[int] = None
    preco_custo: Decimal
    preco_venda: Decimal
    preco_prazo: Decimal
    estoque_atual: Decimal
    estoque_minimo: Optional[Decimal] = 0
    ativo: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ==================== CLIENTES ====================
class ClienteCreate(BaseModel):
    nome: str
    tipo_pessoa: str = "F"
    cpf_cnpj: Optional[str] = None
    rg_ie: Optional[str] = None
    telefone: Optional[str] = None
    telefone2: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    whatsapp: Optional[str] = None
    limite_credito: Optional[Decimal] = 0
    observacao: Optional[str] = None

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: Optional[bool] = None

class ClienteResponse(BaseModel):
    id: int
    empresa_id: int
    nome: str
    tipo_pessoa: str
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    whatsapp: Optional[str] = None
    ativo: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ==================== FORNECEDORES ====================
class FornecedorCreate(BaseModel):
    nome: str
    tipo_pessoa: str = "J"
    cpf_cnpj: Optional[str] = None
    ie: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    contato_nome: Optional[str] = None
    contato_telefone: Optional[str] = None

class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: Optional[bool] = None

class FornecedorResponse(BaseModel):
    id: int
    empresa_id: int
    nome: str
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: bool
    created_at: datetime
    class Config:
        from_attributes = True