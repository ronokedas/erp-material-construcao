"""
API - Autenticação (Login, Usuários)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    verificar_senha, gerar_hash_senha, criar_token_jwt, get_current_user
)
from app.core.config import settings
from app.core.dependencies import get_admin_user
from app.models.auth_models import Usuario, Permissao, UsuarioPermissao
from app.schemas.auth_schemas import (
    LoginRequest, TokenResponse, UsuarioCreate, UsuarioUpdate, UsuarioResponse
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Autentica usuário e retorna token JWT."""
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()

    if not usuario or not verificar_senha(request.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo"
        )

    access_token = criar_token_jwt(
        dados={"sub": usuario.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        usuario=UsuarioResponse.model_validate(usuario)
    )


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Retorna dados do usuário logado."""
    return current_user


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Lista todos os usuários da empresa (admin only)."""
    return db.query(Usuario).filter(
        Usuario.empresa_id == current_user.empresa_id
    ).all()


@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def criar_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_admin_user)
):
    """Cria um novo usuário."""
    usuario = Usuario(
        empresa_id=current_user.empresa_id,
        nome=data.nome,
        email=data.email,
        cpf=data.cpf,
        telefone=data.telefone,
        senha_hash=gerar_hash_senha(data.senha),
        admin=data.admin
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario