from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.infrastructure.auth.jwt_service import JWTService
from app.adapters.dependencies.container import get_auth_service
from app.application.services.auth_service import AuthService
from app.domain.models.usuario import Rol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        jwt_service = JWTService()
        payload = jwt_service.verify_token(token)
        if payload.get("type") != "access":
            raise ValueError("Token invalido")
        usuario_id = int(payload["sub"])
        usuario = auth_service.obtener_usuario_por_id(usuario_id)
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def solo_admin(current_user=Depends(get_current_user)):
    if not current_user.es_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador",
        )
    return current_user


def solo_operador(current_user=Depends(get_current_user)):
    if not current_user.es_operador():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de operador o administrador",
        )
    return current_user
