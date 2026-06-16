"""
Modelos SQLAlchemy - Sistema (Empresa, Config, Logs)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Empresa(Base):
    __tablename__ = "sys_empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200))
    cnpj = Column(String(18), unique=True, nullable=False)
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
    logo = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("Usuario", back_populates="empresa")


class Configuracao(Base):
    __tablename__ = "sys_config"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"), nullable=False)
    chave = Column(String(100), nullable=False)
    valor = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class LogAuditoria(Base):
    __tablename__ = "log_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("sys_empresas.id"))
    usuario_id = Column(Integer, ForeignKey("auth_usuarios.id"))
    acao = Column(String(50), nullable=False)
    entidade = Column(String(50), nullable=False)
    entidade_id = Column(Integer)
    valores_antigos = Column(JSON)
    valores_novos = Column(JSON)
    ip = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)