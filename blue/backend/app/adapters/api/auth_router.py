from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from app.application.services.auth_service import AuthService
from app.adapters.dependencies.container import get_auth_service
from app.adapters.dependencies.auth_dependency import get_current_user, solo_admin

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


class RegistroRequest(BaseModel):
    nombre: str
    email: str
    password: str
    rol: Optional[str] = "cliente"


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/registro", summary="Registrar nuevo usuario")
def registro(data: RegistroRequest, service: AuthService = Depends(get_auth_service)):
    try:
        usuario = service.registrar(
            nombre=data.nombre,
            email=data.email,
            password=data.password,
            rol=data.rol,
        )
        return {"id": usuario.id, "nombre": usuario.nombre,
                "email": usuario.email, "rol": usuario.rol}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.post("/login", summary="Iniciar sesion (OAuth2)")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    try:
        return service.login(email=form_data.username, password=form_data.password)
    except ValueError as e:
        raise HTTPException(401, detail=str(e))


@router.post("/refresh", summary="Renovar access token")
def refresh(data: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    try:
        return service.refresh(data.refresh_token)
    except ValueError as e:
        raise HTTPException(401, detail=str(e))


@router.get("/me", summary="Ver mi perfil")
def me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "nombre": current_user.nombre,
            "email": current_user.email, "rol": current_user.rol}


@router.get("/usuarios", summary="Listar usuarios (solo admin)")
def listar_usuarios(
    current_user=Depends(solo_admin),
    service: AuthService = Depends(get_auth_service),
):
    return service.listar_usuarios()


@router.delete("/usuarios/{id}", summary="Eliminar usuario (solo admin)")
def eliminar_usuario(
    id: int,
    current_user=Depends(solo_admin),
    service: AuthService = Depends(get_auth_service),
):
    try:
        service.eliminar_usuario(id)
        return {"mensaje": "Usuario eliminado"}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))

class SeguridadRequest(BaseModel):
    pregunta: str
    respuesta: str

class PreguntaRequest(BaseModel):
    email: str

class RecuperarRequest(BaseModel):
    email: str
    respuesta: str
    nueva_password: str

@router.post("/seguridad", summary="Configurar pregunta de seguridad")
def configurar_seguridad(
    data: SeguridadRequest,
    current_user=Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    try:
        service.configurar_seguridad(current_user.id, data.pregunta, data.respuesta)
        return {"mensaje": "Pregunta de seguridad configurada"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.post("/pregunta", summary="Obtener pregunta de seguridad por email")
def obtener_pregunta(
    data: PreguntaRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        pregunta = service.obtener_pregunta(data.email)
        return {"pregunta": pregunta}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))

@router.post("/recuperar", summary="Recuperar password con pregunta de seguridad")
def recuperar_password(
    data: RecuperarRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        service.recuperar_password(data.email, data.respuesta, data.nueva_password)
        return {"mensaje": "Contraseña actualizada correctamente"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))