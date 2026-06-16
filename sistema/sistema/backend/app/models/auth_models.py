"""
Modelos SQLAlchemy - Autenticação e Permissões
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "auth_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    cpf = Column(String(14), unique=True)
    telefone = Column(String(20))
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    empresa = relationship("Empresa", back_populates="usuarios")
    permissoes = relationship("UsuarioPermissao", back_populates="usuario", cascade="all, delete-orphan")


class Permissao(Base):
    __tablename__ = "auth_permissoes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    modulo = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("UsuarioPermissao", back_populates="permissao")


class UsuarioPermissao(Base):
    __tablename__ = "auth_usuarios_permissoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id", ondelete="CASCADE"), nullable=False)
    permissao_id = Column(Integer, ForeignKey("auth_permissoes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="permissoes")
    permissao = relationship("Permissao", back_populates="usuarios")