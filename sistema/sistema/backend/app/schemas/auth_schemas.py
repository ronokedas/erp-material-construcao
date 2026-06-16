"""
Schemas Pydantic - Autenticação
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    email: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioResponse"


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    senha: str
    admin: bool = False


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    ativo: Optional[bool] = None


class UsuarioResponse(BaseModel):
    id: int
    empresa_id: int
    nome: str
    email: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    ativo: bool
    admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PermissaoResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    descricao: Optional[str] = None
    modulo: str

    class Config:
        from_attributes = True