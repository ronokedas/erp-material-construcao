"""
Dependências compartilhadas entre as rotas.
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth_models import Usuario


def get_admin_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verifica se o usuário é administrador."""
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem acessar este recurso"
        )
    return current_user


def get_empresa_id(
    current_user: Usuario = Depends(get_current_user)
) -> int:
    """Retorna o ID da empresa do usuário atual."""
    return current_user.empresa_id